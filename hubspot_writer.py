import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from nationality_mapper import normalize_nationality

load_dotenv()

HUBSPOT_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
BASE_URL = "https://api.hubapi.com"

if not HUBSPOT_TOKEN:
    raise RuntimeError("HUBSPOT_ACCESS_TOKEN missing in .env")

HEADERS_JSON = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json",
}

HEADERS_FILE = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
}

# -------------------------------------------------
# Lead status mapping (HubSpot allowed values)
# -------------------------------------------------
LEAD_STATUS_MAP = {
    "neu": "Neu",
    "in beratung": "In Beratung",
    "beratung": "In Beratung",
    "termin vereinbart": "Termin vereinbart",
    "termin vorgeschlagen": "Termin vorgeschlagen",
    "kunde gewonnen": "Kunde gewonnen",
    "bestandskunde": "Bestandskunde",
    "kein interesse": "Kein Interesse",
    "wiedervorlage": "Wiedervorlage",
    "bewerber": "Bewerber",
    "kooperationspartner": "Kooperationspartner",
    "beim setter": "Beim Setter",
}

# -------------------------------------------------
# Normalizers
# -------------------------------------------------
def normalize_expat(value):
    if value is None:
        return "false"
    v = str(value).strip().lower()
    return "true" if v in ["true", "yes", "ja", "1"] else "false"


def normalize_lead_status(value):
    if not value:
        return None
    return LEAD_STATUS_MAP.get(str(value).strip().lower())


# -------------------------------------------------
# HubSpot helpers
# -------------------------------------------------
def get_contact_id_by_email(email: str):
    url = f"{BASE_URL}/crm/v3/objects/contacts/search"
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email.strip().lower()
            }]
        }]
    }

    r = requests.post(url, headers=HEADERS_JSON, json=payload, timeout=30)
    r.raise_for_status()

    results = r.json().get("results", [])
    return results[0]["id"] if results else None


def update_contact(contact_id: str, properties: dict):
    if not properties:
        return

    url = f"{BASE_URL}/crm/v3/objects/contacts/{contact_id}"
    r = requests.patch(
        url,
        headers=HEADERS_JSON,
        json={"properties": properties},
        timeout=30
    )

    if not r.ok:
        print(" HubSpot update failed:", r.status_code, r.text)
        print("Payload:", json.dumps(properties, indent=2, ensure_ascii=False))
        r.raise_for_status()


# -------------------------------------------------
# File upload
# -------------------------------------------------
def upload_file_to_hubspot(audio_path: str):
    url = f"{BASE_URL}/files/v3/files"

    filename = os.path.basename(audio_path)

    data = {
        "folderPath": "/email-audio",
        "options": json.dumps({"access": "PRIVATE"}),
    }

    with open(audio_path, "rb") as f:
        files = {"file": (filename, f)}
        print(" Uploading audio to HubSpot Files...")
        r = requests.post(url, headers=HEADERS_FILE, files=files, data=data, timeout=60)

    if not r.ok:
        print(" File upload failed:", r.status_code, r.text)
        r.raise_for_status()

    j = r.json()
    print(f" File uploaded. id={j.get('id')} name={filename}")
    return j.get("id")


# -------------------------------------------------
# Notes (Attachments section)
# -------------------------------------------------
def create_note_with_attachment(contact_id: str, file_id: str, transcript: str, data: dict):
    url = f"{BASE_URL}/crm/v3/objects/notes"

    logs = [
        "Audio processed from email.",
        f"Job title → {data.get('jobtitle', 'N/A')}",
        f"Nationality → {data.get('nationality', 'N/A')}",
        f"Expat → {data.get('expat', 'N/A')}",
        f"Interested products → {data.get('interested_products', 'N/A')}",
        f"Lead status → {data.get('lead_status', 'N/A')}",
        f"Audio file ID → {file_id}",
    ]

    note_body = "\n".join(logs)

    if transcript:
        note_body += f"\n\n--- Transcript ---\n{transcript}"

    payload = {
        "properties": {
            "hs_note_body": note_body,
            "hs_timestamp": datetime.utcnow().isoformat() + "Z",
            "hs_attachment_ids": str(file_id),
        },
        "associations": [{
            "to": {"id": str(contact_id)},
            "types": [{
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 202  # Note → Contact
            }]
        }]
    }

    print("📎 Attaching file to contact via Note...")
    r = requests.post(url, headers=HEADERS_JSON, json=payload, timeout=30)

    if not r.ok:
        print(" Note creation failed:", r.status_code, r.text)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        r.raise_for_status()

    print(" Note created (Attachments updated)")


# -------------------------------------------------
# Main entry
# -------------------------------------------------
def save_transcript_to_hubspot(email: str, transcript: str, audio_path: str, data: dict):
    print(f" Looking up HubSpot contact for: {email}")

    contact_id = get_contact_id_by_email(email)
    if not contact_id:
        print(" Contact not found in HubSpot")
        return

    props = {}

    if data.get("jobtitle"):
        props["jobtitle"] = data["jobtitle"]

    nationality = normalize_nationality(data.get("nationality"))
    if nationality:
        props["nationalitat"] = nationality

    props["expat"] = normalize_expat(data.get("expat"))

    if data.get("interested_products"):
        props["interesse"] = data["interested_products"]

    lead_status = normalize_lead_status(data.get("lead_status"))
    if lead_status:
        props["hs_lead_status"] = lead_status
    elif data.get("lead_status"):
        print(" Lead status not mapped, skipped")

    update_contact(contact_id, props)

    for k, v in props.items():
        print(f" {k} updated → {v}")

    file_id = upload_file_to_hubspot(audio_path)

    create_note_with_attachment(contact_id, file_id, transcript, data)

    print(" HubSpot update complete\n")

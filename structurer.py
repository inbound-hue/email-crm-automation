import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_structured_data(transcript: str) -> dict:
    schema = {
        "jobtitle": "",
        "nationality": "",
        "expat": "",
        "interested_products": "",
        "lead_status": "",
        "appointment_date": ""
    }

    prompt = (
        "Extract CRM information from the transcript.\n"
        "Return ONLY valid JSON.\n\n"
        "Rules:\n"
        "- Transcript may be German or English\n"
        "- appointment_date must be a human-readable date (e.g. 11 December 2024)\n"
        "- expat must be 'true' or 'false'\n\n"
        "JSON schema:\n"
        + json.dumps(schema, indent=2)
        + "\n\nTranscript:\n"
        + transcript
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You extract CRM-ready structured data."},
            {"role": "user", "content": prompt},
        ],
    )

    raw = resp.choices[0].message.content.strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return schema

    data = json.loads(match.group(0))

    for k in schema:
        data.setdefault(k, "")

    if str(data["expat"]).lower() in ["yes", "ja", "true", "1"]:
        data["expat"] = "true"
    else:
        data["expat"] = "false"

    return data

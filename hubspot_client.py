import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HUBSPOT_BASE = "https://api.hubapi.com"

# Read HubSpot token safely
TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

if not TOKEN:
    raise ValueError(
        "❌ HUBSPOT_ACCESS_TOKEN is missing.\n"
        "Add it to your .env file like this:\n\n"
        "HUBSPOT_ACCESS_TOKEN=pat-xxxxxx\n"
    )

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def list_recent_calls(limit: int = 10) -> List[Dict]:
    """
    Fetch recent call objects from HubSpot, including the recording URL.

    Parameters:
    - limit (int): Number of calls to fetch from HubSpot (default is 10).

    Returns:
    - List[Dict]: A list of call objects with relevant properties.
    """
    url = f"{HUBSPOT_BASE}/crm/v3/objects/calls"

    params = {
        "limit": limit,
        "properties": [
            "hs_call_title",
            "hs_call_recording_url",
            "hs_call_duration",
            "hs_call_to_number",
            "hs_call_from_number"
        ],
        "archived": False,
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=60)
        r.raise_for_status()  # Ensure we raise an error for any non-2xx status codes
    except requests.exceptions.HTTPError as err:
        if r.status_code == 401:
            raise PermissionError(
                " HubSpot returned 401 Unauthorized.\n"
                "Fix:\n"
                "1. Go to HubSpot > Settings > Integrations > Private Apps\n"
                "2. Open your Private App\n"
                "3. Enable these scopes:\n"
                "   - crm.objects.calls.read\n"
                "   - crm.objects.calls.write\n"
                "   - crm.objects.contacts.read\n"
                "4. After enabling scopes, click 'Regenerate Token'\n"
                "5. Update your .env with the NEW token\n"
            )
        print(f"❌ HTTP error: {err}")
        raise err
    except Exception as err:
        print(f"❌ Error occurred: {err}")
        raise err

    return r.json().get("results", [])


def download_audio(recording_url: str, out_path: str) -> bool:
    """
    Download an audio file from the provided HubSpot recording URL.

    Parameters:
    - recording_url (str): URL of the audio recording to be downloaded.
    - out_path (str): Local path to save the downloaded audio file.

    Returns:
    - bool: True if the download was successful, False otherwise.
    """
    try:
        with requests.get(recording_url, stream=True, timeout=300) as r:
            if r.status_code != 200:
                print(f"❌ Failed to download audio ({r.status_code})")
                return False

            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)
        print(f"✅ Audio saved to {out_path}")
        return True
    except Exception as e:
        print(f"❌ Audio download error: {e}")
        return False


def extract_call_meta(call_obj: Dict) -> Dict:
    """
    Extracts relevant metadata from a HubSpot call object, including the call's
    title, recording URL, duration, and phone numbers involved.

    Parameters:
    - call_obj (Dict): The call object returned from HubSpot API.

    Returns:
    - Dict: A dictionary containing extracted call metadata.
    """
    props = call_obj.get("properties", {}) or {}

    return {
        "id": call_obj.get("id"),
        "title": props.get("hs_call_title", ""),
        "recording_url": props.get("hs_call_recording_url"),
        "duration": props.get("hs_call_duration"),
        "to": props.get("hs_call_to_number"),
        "from": props.get("hs_call_from_number"),
    }

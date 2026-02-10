import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
BASE_URL = "https://api.hubapi.com"

headers = {"Authorization": f"Bearer {TOKEN}"}

url = f"{BASE_URL}/crm/v3/properties/contacts"
r = requests.get(url, headers=headers, timeout=60)
r.raise_for_status()

props = r.json().get("results", [])
# Print label -> internal name
for p in props:
    label = p.get("label")
    name = p.get("name")
    field_type = p.get("type")
    print(f"{label}  =>  {name}  ({field_type})")

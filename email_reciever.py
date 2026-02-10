import os, base64, pickle
from email import message_from_bytes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from transcriber import transcribe_file
from structurer import extract_structured_data
from hubspot_writer import save_transcript_to_hubspot
from email_writer import send_email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Function to authenticate and get Gmail service
def get_gmail():
    print("Getting Gmail service...")  # Debug print
    creds = pickle.load(open("token_gmail.pickle", "rb")) if os.path.exists("token_gmail.pickle") else None
    if not creds or not creds.valid:
        print("No valid credentials found, re-authenticating...")  # Debug print
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        pickle.dump(creds, open("token_gmail.pickle", "wb"))
    return build("gmail", "v1", credentials=creds)

# Function to process emails based on the target email address
def process_emails(target_email):
    print(f"Processing emails for: {target_email}")  # Debug print
    service = get_gmail()

    msgs = service.users().messages().list(userId="me", q="has:attachment").execute().get("messages", [])
    print(f"Found {len(msgs)} messages with attachments.")  # Debug print

    for m in msgs:
        raw = service.users().messages().get(userId="me", id=m["id"], format="raw").execute()
        msg = message_from_bytes(base64.urlsafe_b64decode(raw["raw"]))
        print(f"Checking message with subject: {msg.get('Subject', '')}")  # Debug print

        if target_email not in (msg.get("Subject", "").lower()):
            continue

        for p in msg.walk():
            if p.get_filename() and p.get_filename().lower().endswith((".mp3", ".wav", ".m4a", ".mp4")):
                audio_path = p.get_filename()
                print(f"Downloading attachment: {audio_path}")  # Debug print
                open(audio_path, "wb").write(p.get_payload(decode=True))

                transcript = transcribe_file(audio_path)
                print(f"Transcript: {transcript[:100]}...")  # Debug print (first 100 chars)

                data = extract_structured_data(transcript)
                print(f"Extracted data: {data}")  # Debug print

                save_transcript_to_hubspot(target_email, transcript, audio_path, data)

                if data["appointment_date"]:
                    send_email(target_email, data["appointment_date"])

# If run directly, we'll trigger the email processing
if __name__ == "__main__":
    target_email = input("Enter the email address you want to process: ").lower()
    process_emails(target_email)









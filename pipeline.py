# pipeline.py
import os
from datetime import datetime
from dotenv import load_dotenv
from hubspot_client import list_recent_calls, download_audio, extract_call_meta
from transcriber import transcribe_file

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def main(limit: int = 5, model_size: str = "base"):
    load_dotenv()  # loads HUBSPOT_ACCESS_TOKEN

    out_dir_audio = "downloads"
    out_dir_text = "transcripts"
    ensure_dir(out_dir_audio)
    ensure_dir(out_dir_text)

    calls = list_recent_calls(limit=limit)
    if not calls:
        print("No calls found.")
        return

    for call in calls:
        meta = extract_call_meta(call)
        call_id = meta["id"]
        recording_url = meta["recording_url"]

        print(f"\n📞 Call ID: {call_id} | Title: {meta['title']}")
        if not recording_url:
            print("   ↪ No recording URL found. Skipping.")
            continue

        audio_path = os.path.join(out_dir_audio, f"call_{call_id}.mp3")
        text_path = os.path.join(out_dir_text, f"call_{call_id}.txt")

        # Skip if we already processed
        if os.path.exists(text_path):
            print("   ↪ Transcript already exists. Skipping.")
            continue

        # 1) Download audio
        print("   ↓ Downloading audio ...")
        ok = download_audio(recording_url, audio_path)
        if not ok:
            print("   ✖ Failed to download audio.")
            continue

        # 2) Transcribe
        try:
            transcript = transcribe_file(audio_path, model_size=model_size)
        except Exception as e:
            print(f"   ✖ Transcription error: {e}")
            continue

        # 3) Save transcript with a small header
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(f"# Call ID: {call_id}\n")
            f.write(f"# Title: {meta['title']}\n")
            f.write(f"# From: {meta['from']}  To: {meta['to']}\n")
            f.write(f"# Duration (s): {meta['duration']}\n")
            f.write(f"# Recorded: {datetime.utcnow().isoformat()}Z\n\n")
            f.write(transcript)

        print(f"   ✅ Saved transcript → {text_path}")

if __name__ == "__main__":
    # Change limit or model_size as you like
    main(limit=10, model_size="base")

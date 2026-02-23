from flask import Flask, render_template, request, redirect, url_for
import os
from transcriber import transcribe_file
from structurer import extract_structured_data
from hubspot_writer import save_transcript_to_hubspot
from email_writer import send_email

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"].lower()
        audio_file = request.files["audio"]

        print(f"Received email: {email}")

        if audio_file:
            file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(file_path)

            print(f"Saved audio file: {file_path}")

            # 1️⃣ Transcribe
            transcript = transcribe_file(file_path)
            print("Transcription completed")

            # 2️⃣ Extract structured data
            structured_data = extract_structured_data(transcript)
            print("Structured data extracted")

            # 3️⃣ Update HubSpot
            save_transcript_to_hubspot(email, transcript, file_path, structured_data)
            print("HubSpot updated")

            # 4️⃣ Send confirmation email
            send_email(email, structured_data.get("appointment_date"))
            print("Confirmation email sent")

            return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success")
def success():
    return "Audio processed successfully!"


if __name__ == "__main__":
    app.run(debug=True)




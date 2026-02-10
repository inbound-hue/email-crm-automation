from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import os

# Import functions from email_reciever.py
from email_reciever import process_emails

# Flask app setup
app = Flask(__name__)


# Route for the homepage and form submission
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        target_email = request.form["email"].lower()

        # Debug print to confirm form submission
        print(f"Received email: {target_email}")

        # Start the email processing in the background
        start_email_processing(target_email)  # Run in background

        # Redirect to success page after starting background task
        return redirect(url_for("success"))
    return render_template("index.html")  # render the index.html page


# Route for successful email processing
@app.route("/success")
def success():
    return "Email processing was successful!"


# Function to start the email processing in a background thread
def start_email_processing(target_email):
    print(f"Starting email processing in background for: {target_email}")  # Debug print
    thread = Thread(target=process_emails, args=(target_email,))
    thread.start()


# Run the app
if __name__ == "__main__":
    app.run(debug=True)





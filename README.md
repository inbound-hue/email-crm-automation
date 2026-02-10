# Email CRM Automation (Flask)

This project runs a small Flask web app where you enter an email address, and the system processes emails in the background (Gmail API), structures the content, and can write results to HubSpot and use OpenAI for processing.

---

## 1) Requirements (install these first)

### ✅ Windows
- Install **Python 3.11** (recommended)
  - Download: https://www.python.org/downloads/
  - While installing, tick ✅ “Add Python to PATH”
- Install **Git**
  - https://git-scm.com/downloads

### ✅ macOS / Linux
- Python 3.11+
- Git

---

## 2) Download the project from GitHub

Open Terminal / PowerShell and run:

```bash
git clone https://github.com/inbound-hue/email-crm-automation.git
cd email-crm-automation


3) Create and activate a virtual environment
 Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1


If PowerShell blocks activation, run this once:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


Then activate again:

.\.venv\Scripts\Activate.ps1

 Windows CMD
python -m venv .venv
.\.venv\Scripts\activate.bat

✅ macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

4) Install Python libraries
pip install -r requirements.txt

5) Add your API Keys (IMPORTANT)

Never hardcode API keys inside code or commit them to GitHub.

Create a file named .env in the project root (same folder as main.py) and add:

OPENAI_API_KEY=your_openai_key_here
HUBSPOT_ACCESS_TOKEN=your_hubspot_token_here
EMAIL_SENDER=your_email_here
EMAIL_PASSWORD=your_password_or_app_password_here


 TThe .gitignore already blocks .env, so it won’t be uploaded to GitHub.

6) Gmail API Setup (Google OAuth)

This project uses Gmail OAuth. You must have a Google Cloud project with Gmail API enabled and an OAuth client.

Steps (Google Cloud Console)

Go to Google Cloud Console

Enable Gmail API

Create OAuth credentials (Desktop App)

Download credentials.json

Put credentials.json in the project root folder

✅ The project will generate a token file on first login (example: token_gmail.pickle).

First run OAuth login

When you run the program, you may see a link like:

Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth
...

Open it in your browser, allow access, and the app will continue.

If Google redirects and shows “500 error”, usually the local redirect port is blocked or the browser session is confused.
Fix:

Use an Incognito window

Make sure you are logged into the correct Google account

Try again

7) Run the application
python main.py


Then open in browser:

http://127.0.0.1:5000


Enter an email address and submit.

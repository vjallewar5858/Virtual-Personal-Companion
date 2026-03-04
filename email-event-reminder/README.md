# 📅 Email Event Reminder

> An intelligent web application that automatically scans your Gmail inbox, detects event details, sends reminders via **Email & SMS**, and syncs events to **Google Calendar** — built with Python, Streamlit, Twilio & Google APIs.

![CI](https://github.com/YOUR_USERNAME/email-event-reminder/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📧 **Gmail IMAP Scanning** | Connects securely to your inbox and scans all emails |
| 🔍 **Smart Event Detection** | Extracts event date & location using regex pattern matching |
| 📬 **Email Reminders** | Sends a rich HTML reminder email with travel booking links |
| 📱 **SMS Notifications** | Sends instant SMS alerts via Twilio |
| 🗓 **Google Calendar Sync** | Auto-creates calendar events with reminders |
| ⏰ **Configurable Timing** | Choose how many days before to send reminders (1–7) |
| 🌐 **Travel Link Integration** | RedBus, IRCTC, MakeMyTrip & Goibibo links in every reminder |
| 🖥️ **Web Interface** | Clean Streamlit UI — no terminal knowledge needed |

---

## 📂 Project Structure

```
email-event-reminder/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── email_service.py        # Gmail IMAP reading & SMTP sending
│   ├── calendar_service.py     # Google Calendar OAuth2 & event creation
│   ├── sms_service.py          # Twilio SMS integration
│   └── utils.py                # Validation & helper functions
│
├── tests/
│   ├── __init__.py
│   └── test_app.py             # Unit tests (pytest)
│
├── docs/
│   └── setup_guide.md          # Step-by-step setup instructions
│
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI pipeline
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/email-event-reminder.git
cd email-event-reminder
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Fill in your Twilio credentials in .env
```

### 4. Set up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable **Google Calendar API**
3. Create **OAuth 2.0 Client ID** credentials (Desktop app)
4. Download the `client_secret.json` file
5. Place it in the project root *(it is git-ignored)*

### 5. Generate a Gmail App Password

1. Google Account → **Security** → **2-Step Verification** → **App Passwords**
2. Generate a password for "Mail"
3. Use this 16-character password in the app

### 6. Run the app

```bash
streamlit run app.py
```

---

## 📧 Email Format

For the app to detect an event, your email body must contain:

```
Date: DD/MM/YYYY
Location: <venue name>
```

**Example email body:**
```
Hi,

You are invited to the Annual Tech Fest.

Date: 15/03/2025
Location: VJTI Auditorium, Mumbai

Please confirm your attendance.
```

---

## 🔧 Configuration

| Variable | Description |
|---|---|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number (e.g. `+19382016372`) |
| `GOOGLE_CLIENT_SECRET_PATH` | Path to your Google OAuth2 JSON |
| `DEFAULT_TIMEZONE` | Timezone for calendar events (default: `Asia/Kolkata`) |
| `REMINDER_DAYS_BEFORE` | Days before event to send reminder (default: `2`) |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🏗 Architecture

```
Gmail Inbox
     │
     ▼ IMAP SSL
┌─────────────────┐
│  Email Parser   │  ◄── regex: Date + Location
└────────┬────────┘
         │
    ┌────┴──────────────────────────┐
    │                               │
    ▼                               ▼
SMTP Email Reminder          Google Calendar API
(HTML template +             (OAuth2 → event created
 travel links)                with reminders)
    │
    ▼
Twilio SMS
(instant notification)
```

---

## 👥 Team

This project was built as a Final Year B.E. Project.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the web framework
- [Twilio](https://www.twilio.com/) for SMS API
- [Google Calendar API](https://developers.google.com/calendar) for calendar sync
- [Google OAuth2](https://developers.google.com/identity/protocols/oauth2) for authentication

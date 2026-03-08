# Virtual Personal Companion

> An intelligent web application that automatically scans your Gmail inbox, detects event details, sends reminders via **Email & SMS**, and syncs events to **Google Calendar** — built with Python, Streamlit, Twilio & Google APIs.

---

## Features

| Feature | Description |
|---|---|
| **Gmail IMAP Scanning** | Connects securely to your inbox and scans all emails |
| **Smart Event Detection** | Extracts event date & location using regex pattern matching |
| **Email Reminders** | Sends a rich HTML reminder email with travel booking links |
| **SMS Notifications** | Sends instant SMS alerts via Twilio |
| **Google Calendar Sync** | Auto-creates calendar events with reminders |
| **Configurable Timing** | Choose how many days before to send reminders (1–7) |
| **Travel Link Integration** | RedBus, IRCTC, MakeMyTrip & Goibibo links in every reminder |
| **Web Interface** | Clean Streamlit UI — no terminal knowledge needed |

---

## Project Structure

```
Virtual Personal Companion/
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


## Architecture

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

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web framework
- [Twilio](https://www.twilio.com/) for SMS API
- [Google Calendar API](https://developers.google.com/calendar) for calendar sync
- [Google OAuth2](https://developers.google.com/identity/protocols/oauth2) for authentication

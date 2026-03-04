"""
Email Service
Handles Gmail IMAP reading and SMTP sending.
"""

import re
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Pattern to match: Date: DD/MM/YYYY and Location: <value>
EVENT_PATTERN = re.compile(
    r"Date:\s*(\d{1,2}/\d{1,2}/\d{4})\s+Location:\s*([^\n]+)",
    re.DOTALL | re.IGNORECASE,
)


def extract_event_details(msg) -> tuple[str | None, str | None]:
    """
    Parse an email message object and extract event date + location.
    Returns (event_date_str, event_location) or (None, None).
    """
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/plain", "text/html"):
                if "attachment" in str(part.get("Content-Disposition", "")):
                    continue
                payload = part.get_payload(decode=True)
                if payload:
                    result = _parse_payload(payload.decode(errors="ignore"))
                    if result != (None, None):
                        return result
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return _parse_payload(payload.decode(errors="ignore"))
    return None, None


def _parse_payload(text: str) -> tuple[str | None, str | None]:
    match = EVENT_PATTERN.search(text)
    if match:
        raw_date = match.group(1).strip()
        location = match.group(2).strip()
        try:
            event_date = datetime.strptime(raw_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None, None
        return event_date, location
    return None, None


def send_event_reminder_email(
    event_date: str,
    event_location: str,
    sender_email: str,
    receiver_email: str,
    smtp_password: str,
    reminder_days_before: int = 2,
) -> None:
    """Compose and send a rich HTML reminder email."""
    subject = f"🗓 Event Reminder: Upcoming event on {event_date}"
    html_body = _build_html_email(event_date, event_location, reminder_days_before)

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def _build_html_email(event_date: str, event_location: str, reminder_days: int) -> str:
    return f"""
    <html><body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px;">
      <div style="max-width:600px;margin:auto;background:#fff;border-radius:10px;
                  box-shadow:0 2px 8px rgba(0,0,0,0.1);padding:30px;">
        <h2 style="color:#4A90E2;">📅 Event Reminder</h2>
        <p>Hello! You have an upcoming event:</p>
        <table style="width:100%;background:#f0f4ff;border-radius:8px;padding:16px;margin:16px 0;">
          <tr><td><strong>📅 Date:</strong></td><td>{event_date}</td></tr>
          <tr><td><strong>📍 Location:</strong></td><td>{event_location}</td></tr>
          <tr><td><strong>⏰ Reminder:</strong></td>
              <td>This reminder was sent {reminder_days} day(s) in advance</td></tr>
        </table>
        <h3 style="color:#555;">🚌 Plan Your Travel</h3>
        <ul>
          <li>🚌 <a href="https://www.redbus.in/">Book Bus Tickets - RedBus</a></li>
          <li>🚂 <a href="https://www.irctc.co.in/nget/train-search">Book Train Tickets - IRCTC</a></li>
          <li>✈️ <a href="https://www.makemytrip.com/">Book Flights & Hotels - MakeMyTrip</a></li>
          <li>🏨 <a href="https://www.goibibo.com/">Find Hotels - Goibibo</a></li>
        </ul>
        <hr style="margin:24px 0;border:none;border-top:1px solid #eee;">
        <p style="color:#999;font-size:12px;">
          This is an automated reminder from the Email Event Reminder app.
        </p>
      </div>
    </body></html>
    """

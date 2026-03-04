"""
Google Calendar Service
Handles OAuth2 authentication and event creation.
"""

import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH = "token.json"
CALENDAR_ID = "primary"


def get_google_calendar_service(client_secret_path: str = "client_secret.json"):
    """
    Authenticate with Google Calendar API using OAuth2.
    Returns a service object ready to use.
    """
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def add_event_to_google_calendar(
    service,
    event_summary: str,
    event_location: str,
    start_time: str,
    end_time: str,
    timezone: str = "Asia/Kolkata",
) -> str:
    """
    Create a Google Calendar event.
    Returns the HTML link to the created event.
    """
    event_body = {
        "summary": event_summary,
        "location": event_location,
        "description": "Event automatically synced by Email Event Reminder App.",
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60 * 2},  # 2 days before
                {"method": "popup", "minutes": 60},            # 1 hour before
            ],
        },
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
    return created.get("htmlLink", "")


def list_upcoming_events(service, max_results: int = 10) -> list[dict]:
    """Fetch upcoming events from the primary calendar."""
    from datetime import datetime, timezone as tz
    now = datetime.now(tz.utc).isoformat()
    result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return result.get("items", [])

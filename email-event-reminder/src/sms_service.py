"""
SMS Service
Handles Twilio SMS sending with configurable credentials.
"""

import os
from twilio.rest import Client


def get_twilio_client() -> Client:
    """
    Build a Twilio client from environment variables.
    Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in your .env file.
    """
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        raise EnvironmentError(
            "Twilio credentials not found. "
            "Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in your .env file."
        )

    return Client(account_sid, auth_token)


def send_sms(message: str, to_number: str) -> str:
    """
    Send an SMS using Twilio.
    Returns the message SID on success.
    Raises on failure.
    """
    client = get_twilio_client()
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")

    if not from_number:
        raise EnvironmentError("TWILIO_PHONE_NUMBER not set in environment.")

    result = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number,
    )
    return result.sid


def send_bulk_sms(message: str, to_numbers: list[str]) -> list[str]:
    """Send the same SMS to multiple recipients."""
    sids = []
    for number in to_numbers:
        try:
            sid = send_sms(message, number)
            sids.append(sid)
        except Exception as e:
            print(f"Failed to send SMS to {number}: {e}")
    return sids

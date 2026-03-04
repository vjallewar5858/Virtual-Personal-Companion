"""
Utility Functions
"""

import re


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate international phone number format (e.g. +918421540669)."""
    pattern = r"^\+\d{10,15}$"
    return bool(re.match(pattern, phone))


def format_travel_links() -> str:
    """Return HTML travel booking links."""
    return """
    <ul>
        <li>🚌 <a href="https://www.redbus.in/" target="_blank">Book Bus Tickets — RedBus</a></li>
        <li>🚂 <a href="https://www.irctc.co.in/nget/train-search" target="_blank">Book Train Tickets — IRCTC</a></li>
        <li>✈️ <a href="https://www.makemytrip.com/" target="_blank">Book Flights — MakeMyTrip</a></li>
        <li>🏨 <a href="https://www.goibibo.com/" target="_blank">Find Hotels — Goibibo</a></li>
    </ul>
    """


def parse_event_date(raw_date: str) -> str | None:
    """
    Try to parse a date string from common formats.
    Returns ISO format YYYY-MM-DD or None.
    """
    from datetime import datetime
    formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(raw_date.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def days_until(event_date_str: str) -> int | None:
    """Returns the number of days until a given ISO date, or None if parsing fails."""
    from datetime import date
    try:
        event = date.fromisoformat(event_date_str)
        return (event - date.today()).days
    except ValueError:
        return None

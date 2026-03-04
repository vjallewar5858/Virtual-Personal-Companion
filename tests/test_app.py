"""
Unit Tests for Email Event Reminder
Run with: pytest tests/
"""

import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest

from src.utils import validate_email, validate_phone, parse_event_date, days_until
from src.email_service import extract_event_details, _parse_payload


# ─── Utils Tests ──────────────────────────────────────────────────────────────────

class TestValidateEmail:
    def test_valid_gmail(self):
        assert validate_email("user@gmail.com") is True

    def test_valid_custom_domain(self):
        assert validate_email("hello@college.edu") is True

    def test_invalid_no_at(self):
        assert validate_email("notanemail") is False

    def test_invalid_empty(self):
        assert validate_email("") is False


class TestValidatePhone:
    def test_valid_indian_number(self):
        assert validate_phone("+918421540669") is True

    def test_valid_us_number(self):
        assert validate_phone("+14155551234") is True

    def test_missing_plus(self):
        assert validate_phone("918421540669") is False

    def test_too_short(self):
        assert validate_phone("+123") is False


class TestParseEventDate:
    def test_dd_mm_yyyy(self):
        assert parse_event_date("15/08/2024") == "2024-08-15"

    def test_iso(self):
        assert parse_event_date("2024-08-15") == "2024-08-15"

    def test_invalid(self):
        assert parse_event_date("not-a-date") is None


# ─── Email Parsing Tests ──────────────────────────────────────────────────────────

class TestParsePayload:
    def test_basic_match(self):
        text = "Hello,\n\nDate: 15/08/2024\nLocation: Pune, Maharashtra\n\nRegards"
        date, loc = _parse_payload(text)
        assert date == "2024-08-15"
        assert "Pune" in loc

    def test_no_match(self):
        date, loc = _parse_payload("This email has no event details.")
        assert date is None
        assert loc is None

    def test_date_with_spaces(self):
        text = "Date:  05/01/2025   Location: Mumbai Central"
        date, loc = _parse_payload(text)
        assert date == "2025-01-05"

    def test_location_with_special_chars(self):
        text = "Date: 20/12/2024\nLocation: VJTI, Matunga, Mumbai - 400019"
        _, loc = _parse_payload(text)
        assert "VJTI" in loc


class TestExtractEventDetails:
    def _make_email(self, body: str, multipart: bool = False) -> email.message.Message:
        if multipart:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(body, "plain"))
        else:
            msg = MIMEText(body, "plain")
        return email.message_from_string(msg.as_string())

    def test_extracts_from_plain(self):
        msg = self._make_email("Date: 10/03/2025\nLocation: Nagpur")
        date, loc = extract_event_details(msg)
        assert date == "2025-03-10"
        assert loc == "Nagpur"

    def test_extracts_from_multipart(self):
        msg = self._make_email("Date: 22/11/2024\nLocation: IIT Bombay", multipart=True)
        date, loc = extract_event_details(msg)
        assert date == "2024-11-22"
        assert "IIT" in loc

    def test_no_event_returns_none(self):
        msg = self._make_email("Just a regular email with no event info.")
        date, loc = extract_event_details(msg)
        assert date is None
        assert loc is None

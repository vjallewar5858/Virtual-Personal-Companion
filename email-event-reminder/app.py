import streamlit as st
import imaplib
import email
import re
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

from src.calendar_service import get_google_calendar_service, add_event_to_google_calendar
from src.email_service import extract_event_details, send_event_reminder_email
from src.sms_service import send_sms
from src.utils import format_travel_links, validate_email, validate_phone

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Email Event Reminder",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session State Init ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "events_found" not in st.session_state:
    st.session_state.events_found = []
if "processed_count" not in st.session_state:
    st.session_state.processed_count = 0

# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True) if os.path.exists("assets/logo.png") else st.title("📅 Event Reminder")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")

    sms_enabled = st.toggle("Enable SMS Reminders", value=True)
    calendar_enabled = st.toggle("Enable Google Calendar Sync", value=True)
    email_reminder_enabled = st.toggle("Enable Email Reminders", value=True)

    st.markdown("---")
    st.markdown("### 📱 SMS Configuration")
    receiver_phone = st.text_input(
        "Receiver Phone (with country code)",
        value="+91XXXXXXXXXX",
        help="e.g. +918421540669"
    )

    st.markdown("---")
    st.markdown("### ⏰ Reminder Timing")
    reminder_days_before = st.slider("Send reminder N days before event", 1, 7, 2)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(
        "This app scans your Gmail inbox for event emails, "
        "sends reminders via email & SMS, and syncs events "
        "to Google Calendar automatically."
    )

# ─── Main UI ─────────────────────────────────────────────────────────────────────
st.title("📬 Email Event Reminder")
st.markdown(
    "Automatically detect events in your Gmail, send reminders, "
    "and sync to Google Calendar — all in one click."
)
st.markdown("---")

# ─── Login Section ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔐 Gmail Login")
    email_address = st.text_input("Gmail Address", placeholder="you@gmail.com")
    app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="xxxx xxxx xxxx xxxx",
        help="Generate from Google Account → Security → App Passwords"
    )

with col2:
    st.subheader("🔑 Google Calendar")
    client_secret_file = st.file_uploader(
        "Upload client_secret.json",
        type="json",
        help="Download from Google Cloud Console → OAuth 2.0 Credentials"
    ) if calendar_enabled else None

    if client_secret_file:
        secret_path = "client_secret.json"
        with open(secret_path, "wb") as f:
            f.write(client_secret_file.read())
        st.success("✅ Client secret loaded!")

st.markdown("---")

# ─── Action Button ────────────────────────────────────────────────────────────────
if st.button("🚀 Scan & Send Reminders", type="primary", use_container_width=True):
    if not email_address or not validate_email(email_address):
        st.error("❌ Please enter a valid Gmail address.")
    elif not app_password:
        st.error("❌ Please enter your Gmail App Password.")
    elif sms_enabled and not validate_phone(receiver_phone):
        st.error("❌ Please enter a valid phone number (e.g. +918421540669)")
    else:
        progress = st.progress(0, text="Connecting to Gmail...")
        status_box = st.empty()
        results_container = st.container()

        try:
            # Connect
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, app_password)
            st.session_state.logged_in = True
            progress.progress(20, text="✅ Connected! Scanning inbox...")

            mail.select("inbox")
            _, messages = mail.search(None, "(ALL)")
            mail_ids = messages[0].split()

            total = len(mail_ids)
            events_found = []
            emails_processed = 0

            for i, mail_id in enumerate(mail_ids):
                progress.progress(20 + int(60 * i / max(total, 1)), text=f"📧 Processing email {i+1}/{total}...")
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                event_date, event_location = extract_event_details(msg)
                emails_processed += 1

                if event_date and event_location:
                    event_info = {
                        "subject": msg.get("Subject", "No Subject"),
                        "from": msg.get("From", "Unknown"),
                        "date": msg.get("Date", ""),
                        "event_date": event_date,
                        "event_location": event_location,
                    }
                    events_found.append(event_info)

                    # Email reminder
                    if email_reminder_enabled:
                        try:
                            send_event_reminder_email(
                                event_date, event_location,
                                email_address, email_address, app_password,
                                reminder_days_before
                            )
                        except Exception as e:
                            st.warning(f"⚠️ Email reminder failed: {e}")

                    # SMS reminder
                    if sms_enabled:
                        try:
                            send_sms(
                                f"🗓 Event Reminder: {event_info['subject']} on {event_date} at {event_location}",
                                receiver_phone
                            )
                        except Exception as e:
                            st.warning(f"⚠️ SMS failed: {e}")

                    # Google Calendar
                    if calendar_enabled and os.path.exists("client_secret.json"):
                        try:
                            service = get_google_calendar_service("client_secret.json")
                            start_time = f"{event_date}T09:00:00"
                            end_time = f"{event_date}T18:00:00"
                            link = add_event_to_google_calendar(
                                service,
                                event_info["subject"],
                                event_location,
                                start_time,
                                end_time
                            )
                            event_info["calendar_link"] = link
                        except Exception as e:
                            st.warning(f"⚠️ Calendar sync failed: {e}")

            st.session_state.events_found = events_found
            st.session_state.processed_count = emails_processed
            progress.progress(100, text="✅ Done!")

        except imaplib.IMAP4.error as e:
            st.error(f"❌ Gmail login failed: {e}")
            progress.empty()
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            progress.empty()
        finally:
            try:
                mail.logout()
            except Exception:
                pass

# ─── Results ─────────────────────────────────────────────────────────────────────
if st.session_state.events_found or st.session_state.processed_count > 0:
    st.markdown("---")
    st.subheader("📊 Results")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("📧 Emails Scanned", st.session_state.processed_count)
    col_b.metric("🎯 Events Found", len(st.session_state.events_found))
    col_c.metric("✅ Reminders Sent", len(st.session_state.events_found))

    if st.session_state.events_found:
        st.markdown("### 🗓 Detected Events")
        for ev in st.session_state.events_found:
            with st.expander(f"📌 {ev['subject']} — {ev['event_date']}"):
                st.markdown(f"**📍 Location:** {ev['event_location']}")
                st.markdown(f"**📨 From:** {ev['from']}")
                st.markdown(f"**📅 Email Date:** {ev['date']}")
                if "calendar_link" in ev:
                    st.markdown(f"**🗓 Calendar:** [View Event]({ev['calendar_link']})")
                st.markdown("**🚌 Travel Links:**")
                st.markdown(format_travel_links(), unsafe_allow_html=True)
    else:
        st.info("No events were detected in your inbox. Make sure emails contain `Date: DD/MM/YYYY` and `Location: ...` fields.")

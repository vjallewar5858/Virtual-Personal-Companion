# 🛠 Setup Guide

This guide walks you through setting up every external service the app depends on.

---

## 1. Gmail App Password

Gmail no longer allows plain passwords for third-party apps. You need an **App Password**.

1. Sign in to your Google Account
2. Go to **Manage your Google Account** → **Security**
3. Under "How you sign in to Google", select **2-Step Verification** (must be enabled)
4. At the bottom of the page, select **App passwords**
5. Choose app: **Mail** | Choose device: **Other (Custom name)** → name it `EventReminder`
6. Click **Generate** — copy the 16-character password
7. Paste it into the app's password field

> ⚠️ Never share or commit your App Password.

---

## 2. Google Calendar API Setup

1. Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Click **Create Project** → give it a name (e.g. `EmailEventReminder`)
3. In the left menu: **APIs & Services** → **Library**
4. Search for **Google Calendar API** → click **Enable**
5. Go to **APIs & Services** → **Credentials**
6. Click **+ Create Credentials** → **OAuth client ID**
7. Application type: **Desktop app** → click **Create**
8. Click **Download JSON** → save as `client_secret.json` in the project folder

> ⚠️ `client_secret.json` is listed in `.gitignore` and will NOT be pushed to GitHub.

On first run, a browser window will open asking you to authorize the app. After authorization, a `token.json` file is saved locally for future use.

---

## 3. Twilio SMS Setup

1. Sign up at [https://www.twilio.com/](https://www.twilio.com/)
2. From the Console dashboard, copy:
   - **Account SID**
   - **Auth Token**
3. Go to **Phone Numbers** → **Get a trial number** (free)
4. Copy the phone number (e.g. `+19382016372`)
5. Add all three values to your `.env` file:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

> ⚠️ Free trial Twilio accounts can only send SMS to **verified phone numbers**. Verify your number in Twilio Console → **Verified Caller IDs**.

---

## 4. Environment Setup

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Then open `.env` and fill in:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

The app loads these automatically at startup.

---

## 5. Running Locally

```bash
# Activate your virtual environment
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 6. Deploying to Streamlit Cloud (Optional)

1. Push your code to GitHub *(make sure `.env` and `*.json` are in `.gitignore`)*
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
3. Connect your GitHub repo
4. In the app settings, add your secrets under **Advanced Settings → Secrets**:

```toml
TWILIO_ACCOUNT_SID = "ACxxx"
TWILIO_AUTH_TOKEN = "xxx"
TWILIO_PHONE_NUMBER = "+1xxx"
```

> Note: For Google Calendar on Streamlit Cloud, you'll need to handle OAuth differently (service account or pre-generated token).

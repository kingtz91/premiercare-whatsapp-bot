
# PremierCare WhatsApp Chatbot 🤖

This is a multilingual WhatsApp chatbot for Premier Care Clinic, supporting **English**, **Swahili**, and **French** via Meta Cloud API.

---

## 🌐 Features

- Language selector (EN, SW, FR)
- Auto-reply for:
  - Consultation Booking
  - Vaccination
  - Self-request Lab Tests
  - Ask for Results
  - Connect to Staff

---

## 🚀 Deployment on Render

### 1. Requirements
- Python 3.10+
- Flask
- Meta WhatsApp Cloud API access
- GitHub account

---

### 2. Deploy via GitHub + Render

1. Push this project to GitHub
2. Go to [https://render.com](https://render.com)
3. Click **New Web Service**
4. Connect your GitHub repo
5. Set:
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python app.py`
6. Deploy

---

## 🔗 Connect to Meta Cloud API

1. Go to [https://developers.facebook.com/apps](https://developers.facebook.com/apps)
2. Select your app
3. Under **Webhooks**:
   - Set webhook URL to your deployed Render URL
   - Use **Verify Token**: `premierverifytoken`
4. Subscribe to these fields:
   - `messages`
   - `message_status`
   - `message_deliveries`

---

## ⚙️ Configuration

In `app.py`, replace these values:

```python
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
PHONE_NUMBER_ID = 'YOUR_PHONE_NUMBER_ID'
```

---

## 🧪 Test

Once connected:
- Add test number from Meta sandbox
- Say "hi" on WhatsApp
- Bot will reply in language of choice

---

## 🏥 Powered by Premier Care Clinic

Visit: [https://www.premiercareclinic.com](https://www.premiercareclinic.com)

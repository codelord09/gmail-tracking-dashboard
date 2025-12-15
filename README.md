# Gmail Tracking Dashboard (Privacy-Focused)

A privacy-first, read-only analytics dashboard that tracks and visualizes your sent email activity without reading email content.

![Dashboard Preview](frontend/public/preview.png)

## Features

- **Privacy First**: Only requests `gmail.readonly` scope. Stores only counts and dates, never email bodies.
- **Sent Email Analytics**:
  - **Volume Tracking**: See how many emails you send daily.
  - **Trends**: Visual line charts for sent and reply trends.
  - **Time Ranges**: "Today", "Last 7 Days", "Last 15 Days", "Last 30 Days".
- **Reply Rate Analysis**:
  - Estimates reply rate by analyzing thread activity.
  - Displays "Avg Reply Rate" and per-day reply counts.
- **Detailed Reporting**:
  - Day-by-day table breakdown of Sent vs. Reply activity.

## Tech Stack

- **Frontend**: React (Vite), TailwindCSS, Recharts.
- **Backend**: Python (FastAPI), SQLAlchemy, Google Client Library.
- **Database**: PostgreSQL.

## Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL** (running locally or remotely)
- **Google Cloud Console Project** with Gmail API enabled.

## Setup Instructions

### 1. Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a Project and enable **Gmail API**.
3. Configure OAuth Consent Screen (Add `https://www.googleapis.com/auth/gmail.readonly` scope).
4. Add yourself to **Test Users**.
5. Create OAuth Client ID (Web Application).
   - **Authorized Redirect URI**: `http://localhost:8000/auth/callback`
6. Download the JSON and save it as `backend/credentials.json`.

### 2. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/gmail_dashboard
OAUTHLIB_INSECURE_TRANSPORT=1
```

*(Replace `user:password` with your PostgreSQL credentials)*

## Running the Project

We have provided a convenient script to start everything at once.

```bash
./start_app.sh
```

This script will:
1. Setup/Activate Python virtual environment.
2. Run database migrations.
3. Start the Backend server (Port 8000).
4. Start the Frontend server (Port 5173).

Visit **http://localhost:5173** to view your dashboard.

## Manual Run (Alternative)

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Authors
- **codelord09** (neerajgupta0192@gmail.com)

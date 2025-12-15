from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import auth
import gmail_service
import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000", # React app
    "http://localhost:5173", # Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Gmail Tracking API"}

@app.get("/login")
def login():
    flow = auth.get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@app.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")
    
    flow = auth.get_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials
    auth.save_credentials(creds)
    
    return RedirectResponse("http://localhost:5173?auth=success")

@app.get("/status")
def status():
    creds = auth.get_credentials()
    return {"authenticated": creds is not None and creds.valid}

@app.post("/sync")
def sync_emails(db: Session = Depends(get_db)):
    creds = auth.get_credentials()
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    stats = gmail_service.fetch_and_store_sent_emails(creds, db)
    return {"status": "success", "synced_days": len(stats) if stats else 0}

@app.get("/stats")
def get_stats(days: int = 30, db: Session = Depends(get_db)):
    # Return last N days
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    
    stats = db.query(models.SentEmailStat).filter(models.SentEmailStat.date >= start_date).order_by(models.SentEmailStat.date).all()
    return stats

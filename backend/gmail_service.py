from googleapiclient.discovery import build
import datetime
from sqlalchemy.orm import Session
from models import SentEmailStat
from database import SessionLocal

def fetch_and_store_sent_emails(creds, db: Session):
    service = build('gmail', 'v1', credentials=creds)
    
    # We want to sync for the last 30 days or so, or just "today" if running daily
    # For simplicity, let's look at the last 30 days
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    
    # query: "from:me label:SENT after:YYYY/MM/DD"
    # Note: Gmail search is strict.
    query = f"from:me label:SENT after:{start_date.strftime('%Y/%m/%d')}"
    
    results = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
    messages = results.get('messages', [])
    
    # We need to get details to check exact date for aggregation
    # Batch request would be better, but simple loop for now (beware rate limits)
    
    # Optimization: To avoid fetching *every* message detail, we rely on the search query
    # catching the right range. But to aggregate by day, we need the timestamp.
    # 'internalDate' is available in list response? No, only id and threadId.
    # We must fetch details or use a more granular search strategy.
    
    # Better strategy: List messages, get 'internalDate' from details. 
    # To reduce quota, we can fetch 'internalDate' only.
    
    stats = {} # date -> count

    if not messages:
        return

    # Batch get
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Google API client supports batch, but it's complex to setup here quickly.
    # Let's iterate. For 500 messages, it might be slow.
    # Let's just do a few for now or assume we can get headers.
    
    # Actually, let's refine the query to count per day? No, API doesn't do aggregation.
    
    # Let's just fetch details for 'internalDate'
    for msg in messages:
        # We need thread details to check for replies
        # This increases API usage.
        thread_id = msg['threadId']
        # msg details (minimal) for date
        m = service.users().messages().get(userId='me', id=msg['id'], format='minimal').execute()
        internal_date = int(m['internalDate']) / 1000
        date_obj = datetime.date.fromtimestamp(internal_date)
        
        # Check thread for replies
        # A thread has a reply if it has more than 1 message. 
        # (Heuristic: If I sent it, and there's another msg, it's likely a reply).
        # To be more accurate, we should check if other messages are NOT from me.
        # But `threads.get` is another API call.
        thread = service.users().threads().get(userId='me', id=thread_id, format='minimal').execute()
        # threads.get with format minimal returns 'messages' list with 'id' snippet...
        # Actually simplest check is number of messages in thread.
        is_replied = len(thread.get('messages', [])) > 1
        
        if date_obj not in stats:
            stats[date_obj] = {'count': 0, 'replied': 0}
        stats[date_obj]['count'] += 1
        if is_replied:
            stats[date_obj]['replied'] += 1
        
    # Store in DB
    for date, data in stats.items():
        existing = db.query(SentEmailStat).filter(SentEmailStat.date == date).first()
        if existing:
            existing.count = data['count']
            existing.replied_count = data['replied']
        else:
            new_stat = SentEmailStat(date=date, count=data['count'], replied_count=data['replied'])
            db.add(new_stat)
    
    db.commit()
    return stats

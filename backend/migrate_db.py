from sqlalchemy import text
from database import engine

def migrate():
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE sent_email_stats ADD COLUMN IF NOT EXISTS replied_count INTEGER DEFAULT 0"))
        conn.commit()
    print("Migration complete: Added replied_count column.")

if __name__ == "__main__":
    migrate()

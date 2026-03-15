from sqlalchemy import inspect, text
from database import engine

def migrate():
    inspector = inspect(engine)
    if "sent_email_stats" not in inspector.get_table_names():
        print("Migration skipped: sent_email_stats table does not exist yet.")
        return

    columns = {column["name"] for column in inspector.get_columns("sent_email_stats")}
    if "replied_count" in columns:
        print("Migration skipped: replied_count column already exists.")
        return

    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE sent_email_stats ADD COLUMN replied_count INTEGER DEFAULT 0"))
    print("Migration complete: Added replied_count column.")

if __name__ == "__main__":
    migrate()

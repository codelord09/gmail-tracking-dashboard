from sqlalchemy import Column, Integer, Date, DateTime
from database import Base
import datetime

class SentEmailStat(Base):
    __tablename__ = "sent_email_stats"

    date = Column(Date, primary_key=True, index=True)
    count = Column(Integer, default=0)
    replied_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

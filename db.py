# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Connection string from Render
DATABASE_URL = os.getenv("DATABASE_URL")  # set in Render env vars

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class MeditationLog(Base):
    __tablename__ = "meditation_log"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    age = Column(String(10))
    mood = Column(String(50))
    context = Column(String(100))
    style = Column(String(50))
    length = Column(String(10))
    journal = Column(Text)
    audio_file = Column(String(100))
    script_file = Column(String(100))

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

def log_request(age, mood, context, style, length, journal, audio_file, script_file):
    session = SessionLocal()
    log = MeditationLog(
        age=age,
        mood=mood,
        context=context,
        style=style,
        length=length,
        journal=journal,
        audio_file=audio_file,
        script_file=script_file
    )
    session.add(log)
    session.commit()
    session.close()
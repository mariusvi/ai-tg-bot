
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import threading


engine = create_engine("sqlite:///db.sqlite", echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = Session()
    return thread_local.session


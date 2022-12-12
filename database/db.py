
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

def start_database():
    global session
    engine = create_engine("sqlite:///db.sqlite", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
from sqlalchemy import Column, String, Integer
from database.orm_base import Base

class Users(Base):
    __tablename__ = "users"

    name = Column("name", String)
    tg_user_name = Column("tg_user_name", String)
    tg_id = Column("tg_id", Integer, primary_key=True)
    chat_id = Column("chat_id", Integer)
    role = Column("role", String)

    def __init__(self, name, tg_user_name, tg_id, chat_id, role):
        self.name = name
        self.tg_user_name = tg_user_name
        self.tg_id = tg_id
        self.chat_id = chat_id
        self.role = role

    def __repr__(self) -> str:
        return f"{self.name} {self.tg_user_name} {self.tg_id} {self.chat_id} {self.role}"


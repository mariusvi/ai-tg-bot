from sqlalchemy import Column, String
from database.orm_base import Base

class Data_sources(Base):
    __tablename__ = "data_sources"

    name = Column("name", String, primary_key=True)
    category = Column("category", String)
    url = Column("url", String)
    description = Column("description", String)
    icon = Column("icon", String)
    
    def __repr__(self) -> str:
        return f"{self.name} {self.category} {self.url} {self.description} {self.icon}"

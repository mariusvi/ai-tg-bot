from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base(metadata=MetaData())
metadata = Base.metadata

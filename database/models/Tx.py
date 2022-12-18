from sqlalchemy import Column, Integer, String, Index
from database.orm_base import Base

class Tx(Base):
    __tablename__ = 'tx'

    accessList = Column(String)
    blockHash = Column(String)
    blockNumber = Column(Integer)
    chainId = Column(String)
    addressFrom = Column(String)
    gas = Column(Integer)
    gasPrice = Column(Integer)
    tx_hash = Column(String, primary_key=True)
    input = Column(String)
    nonce = Column(Integer)
    r = Column(String)
    s = Column(String)
    addressTo = Column(String)
    transactionIndex = Column(Integer)
    type = Column(String)
    v = Column(Integer)
    value = Column(Integer)
    maxFeePerGas = Column(Integer)
    maxPriorityFeePerGas = Column(Integer)

    
    __table_args__ = (
        Index('index_tx', 'blockNumber', 'tx_hash'),
    ) 

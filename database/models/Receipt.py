from sqlalchemy import Column, Integer, String, Index
from database.orm_base import Base


class Receipt(Base):
    __tablename__ = "receipt"

    blockHash = Column(String)
    blockNumber = Column(Integer)
    contractAddress = Column(String)
    cumulativeGasUsed = Column(Integer)
    effectiveGasPrice = Column(Integer)
    fromAddress = Column(String)
    gasUsed = Column(Integer)
    logs = Column(String)
    logsBloom = Column(String)
    status = Column(Integer)
    toAddress = Column(String)
    balanceFrom = Column(Integer)
    balanceTo = Column(Integer)
    tx_hash = Column(String, primary_key=True)
    transactionIndex = Column(Integer)
    type = Column(String)
    root = Column(String)

    __table_args__ = (Index("index_receipt", "fromAddress", "toAddress", "tx_hash"),)

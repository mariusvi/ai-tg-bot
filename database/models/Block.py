from sqlalchemy import Column, Integer, String, Index
from database.orm_base import Base


class Block(Base):
    __tablename__ = "block"

    baseFeePerGas = Column(Integer)
    difficulty = Column(Integer)
    extraData = Column(String)
    gasLimit = Column(Integer)
    gasUsed = Column(Integer)
    blockHash = Column(String)
    logsBloom = Column(String)
    miner = Column(String)
    mixHash = Column(String)
    nonce = Column(String)
    blockNumber = Column(Integer, primary_key=True)
    parentHash = Column(String)
    receiptsRoot = Column(String)
    sha3Uncles = Column(String)
    size = Column(Integer)
    stateRoot = Column(String)
    timestamp = Column(Integer)
    totalDifficulty = Column(String)
    transactions = Column(String)
    transactionsRoot = Column(String)
    uncles = Column(String)

    __table_args__ = (Index("index_block", "timestamp"),)

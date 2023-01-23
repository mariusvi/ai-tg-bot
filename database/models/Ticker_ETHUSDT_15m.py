from sqlalchemy import Column, Integer, Index, Float
from database.orm_base import Base


class Ticker_ETHUSDT_15m(Base):
    __tablename__ = "ticker_ETHUSDT_15m"

    open_time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    close_time = Column(Integer)
    quote_asset_volume = Column(Float)
    number_of_trades = Column(Integer)
    taker_buy_base_asset_volume = Column(Float)
    taker_buy_quote_asset_volume = Column(Float)

    __table_args__ = (Index("index_ticker_ETHUSDT_15m", "open_time", "close_time"),)

    def get_pair(self) -> str:
        return "ETHUSDT"

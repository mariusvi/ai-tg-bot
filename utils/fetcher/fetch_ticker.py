from typing import List
from binance import Client
from database.db import get_session
from database.models.Ticker_ETHUSDT_15m import Ticker_ETHUSDT_15m
from src.config import bnc_api_key, bnc_api_secret


class Fetch_ticker:
    def __init__(self) -> None:
        self._session = get_session()
        self._client = Client(bnc_api_key, bnc_api_secret)

    def fetch_ticker(self, ticker_object: Ticker_ETHUSDT_15m, date: int) -> List:
        ticker = ticker_object()
        print("start")
        with self._session as session:
            all_ticks_in_db_query = session.query(ticker_object.open_time).all()
            all_ticks_in_db = []
            for b in all_ticks_in_db_query:
                d = b._asdict()
                all_ticks_in_db.append(d["open_time"])
            candles = self._client.get_historical_klines(
                ticker.get_pair(), self._client.KLINE_INTERVAL_15MINUTE, date
            )
            for candle in candles:
                if candle[0] not in all_ticks_in_db:
                    session.add(
                        ticker_object(
                            open_time=candle[0],
                            open=candle[1],
                            high=candle[2],
                            low=candle[3],
                            close=candle[4],
                            volume=candle[5],
                            close_time=candle[6],
                            quote_asset_volume=candle[7],
                            number_of_trades=candle[8],
                            taker_buy_base_asset_volume=candle[9],
                            taker_buy_quote_asset_volume=candle[10],
                        )
                    )
            session.commit()

        return candles

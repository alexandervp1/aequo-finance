import mplfinance as mpf
import requests
import pandas as pd
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import engine, local_session
from app.models.financial import Candle
from sqlalchemy.dialects.postgresql import insert


class MarketDataService:
    
    base_url = "https://api.binance.com/api/v3"

    def __init__(self, db_session: Optional[Session] = None):

        self.db = db_session or local_session()

    def cleaned_klines(
            self,
            symbol: str = "BTCUSDT",
            interval: str = "1d", 
            limit: int = "365",
            save_to_db: bool = False
    ): 
        pd.DataFrame

        """
        Main execution flow:
        1. Fetch raw candle data from Binance REST API.
        2. Clean and format timestamps, data types, and column names by default.
        3. Optionally persist the clean DataFrame into PostgreSQL.
        4. Return the cleaned DataFrame.
        """

        endpoint = f"{self.base_url}/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval.lower(),
            "limit": int(limit)
        }

        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        columns = [
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "qav", "trades", "taker_buy_vol", "tbq", "ignore"
        ]

        df = pd.DataFrame(raw_data, columns=columns)

        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        numeric_cols = ["open", "high", "low", "volume", "close"]
        df[numeric_cols] = df[numeric_cols].astype(float)

        df["symbol"] = symbol.upper()
        df["interval"] = interval
        
        df.sort_values("timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)

        if save_to_db and self.db:
            self.save_candle_to_db(df, symbol.upper(), interval.lower())

        return df

    def save_candle_to_db(self, df: pd.DataFrame, symbol: str, interval: str):
        """
        Inserts or updates (upserts) cleaned candle data into PostgreSQL.
        """
        records = df.to_dict(orient="records")

        for row in records:
            chart_updater= insert(Candle).values(
                symbol=symbol,
                interval=interval,
                timestamp=row["timestamp"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"]
            )

            chart_updater = chart_updater.on_conflict_do_update(
                constraint="uq_symbol_interval_timestamp",
                set_={
                    "open": chart_updater.excluded.open,
                    "high": chart_updater.excluded.high,
                    "low": chart_updater.excluded.low,
                    "close": chart_updater.excluded.close,
                    "volume": chart_updater.excluded.volume,
                }
            )
            self.db.execute(chart_updater)

        self.db.commit()


if __name__ == "__main__":

    service = MarketDataService()
    df = service.cleaned_klines(symbol="BTCUSDT", interval="1D", limit=365)

    print("\n--- Datatypes ---")
    print(df.dtypes)

    print("\n--- Market Data ---")
    print(df)

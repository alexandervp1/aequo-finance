import mplfinance as mpf
import requests
import pandas as pd
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import engine, local_session


class MarketDataService:
    
    base_url = "https://api.binance.com/api/v3"

    def __init__(self, db_session: Optional[Session] = None):

        self.db = db_session or local_session

    def cleaned_klines(
            self,
            symbol: str = "BTCUSDT",
            interval: str = "1d", 
            limit: int = "365",
            save_to_db: bool = True
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

        return df


if __name__ == "__main__":

    service = MarketDataService()
    df = service.cleaned_klines(symbol="BTCUSDT", interval="1D", limit=365)

    print("\n--- Datatypes ---")
    print(df.dtypes)

    print("\n--- Market Data ---")
    print(df)

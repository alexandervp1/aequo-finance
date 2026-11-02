import sys
import os

'''Adds rute'''
sys.path.append(os.path.abspath(".."))


import pandas as pd
import mplfinance as mpf
from app.services.market_data import MarketDataService

def chart_gen(df, title ="Crypto Chart"):

    chart_df = df.copy()

    chart_df.set_index("timestamp", inplace = True)

    mpf.plot(
        chart_df,
        type="candle",
        style="charles",
        volume=True,
        title=title,
        figsize=(12,6)
    )


    
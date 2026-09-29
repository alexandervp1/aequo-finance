from app.services.market_data import MarketDataService

service = MarketDataService()

df = service.cleaned_klines(symbol="BTCUSDT", interval='1d', limit=365, save_to_db=True)

print(f'Data succesfully saved to database. Inserted {len(df)} days of BTC market data.')

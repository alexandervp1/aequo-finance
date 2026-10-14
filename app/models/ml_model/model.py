import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier

engine = create_engine('postgresql://postgres:Agent2026@localhost:5432/aequo_db')

query = """
     SELECT timestamp, open, high, low, close, volume
     FROM candles
     WHERE symbol = 'BTCUSDT' AND interval = '1d'
     ORDER BY timestamp ASC;
"""
df = pd.read_sql(query, engine)

df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')

#Feature Engineering
df['return_1d'] = df['close'].pct_change()
df['candle_range'] = (df['high'] - df['low']) / df['close']
df['volume_change'] = df['volume'].pct_change()

df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

df_clean = df.dropna().copy()

feature_cols = ['return_1d', 'candle_range', 'volume_change']
x = df_clean[feature_cols]
y = df_clean['target']

clean_len = len(df_clean)
split_60 = int(0.6 * clean_len)
split_80 = int(0.8 * clean_len)

scaler = StandardScaler()

train_x = x.iloc[:split_60]
valid_x = x.iloc[split_60:split_80]
test_x = x.iloc[split_80:]


train_y = y.iloc[:split_60]
valid_y = y.iloc[split_60:split_80]
test_y = y.iloc[split_80:]

train_scaled = scaler.fit_transform(train_x[feature_cols])
valid_scaled = scaler.transform(valid_x[feature_cols])
test_scaled = scaler.transform(test_x[feature_cols])

knn = KNeighborsClassifier(n_neighbors=5) #K starting from 5  #20 #70
knn.fit(train_scaled, train_y)
y_pred = knn.predict(test_scaled)
print("\n KNN PERFORMANCE: ")
print(classification_report(test_y, y_pred))

print("\n RANDOM FOREST PERFORMANCE: ")
rf = RandomForestClassifier(n_estimators=700, max_depth=7, random_state=42)

rf.fit(train_x, train_y)
rf_pred = rf.predict(test_x)
print(classification_report(test_y, rf_pred))











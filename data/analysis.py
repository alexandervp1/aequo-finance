import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/ps_data.csv", comment="#")

print(df.shape)
print(df.ndim)

marker = df["default_flag"] == 1
planet_marker = df[marker]
print(len(planet_marker))

print(df.iloc[0:101].to_string())

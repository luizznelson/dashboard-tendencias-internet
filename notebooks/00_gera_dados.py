import pandas as pd
import numpy as np

np.random.seed(42)
dias = pd.date_range("2024-01-01", "2024-12-31", freq="D")
base = 10000
# Sazonalidade semanal + tendência de crescimento + ruído
consumo = (
    base
    + 30 * np.sin(2 * np.pi * dias.dayofyear / 7)   # variação semanal
    + 15 * np.sin(2 * np.pi * dias.dayofyear / 365) # variação anual
    + np.linspace(0, 120, len(dias))                # tendência de aumento
    + np.random.normal(0, 25, len(dias))            # ruído
).astype(int)

df = pd.DataFrame({'data': dias, 'consumo_mb': consumo})
df.to_csv("data/internet_usage.csv", index=False)

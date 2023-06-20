import pandas as pd

df = pd.read_parquet('green_tripdata_2023-01.parquet')

print(df.info())
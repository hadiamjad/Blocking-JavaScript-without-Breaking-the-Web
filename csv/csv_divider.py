import pandas as pd
import os

df1 = pd.read_csv(r"tranco.csv")

df = df1.iloc[0:20000, [1]]
df.to_csv(r"1k.csv")
df = df1.iloc[20000:30000, [1]]
df.to_csv(r"2k.csv")
df = df1.iloc[30000:40000, [1]]
df.to_csv(r"3k.csv")
df = df1.iloc[40000:50000, [1]]
df.to_csv(r"4k.csv")
df = df1.iloc[50000:60000, [1]]
df.to_csv(r"5k.csv")
df = df1.iloc[60000:70000, [1]]
df.to_csv(r"6k.csv")
df = df1.iloc[70000:80000, [1]]
df.to_csv(r"7k.csv")
df = df1.iloc[80000:90000, [1]]
df.to_csv(r"8k.csv")
df = df1.iloc[90000:100000, [1]]
df.to_csv(r"9k.csv")
df = df1.iloc[100000:120000, [1]]
df.to_csv(r"10k.csv")

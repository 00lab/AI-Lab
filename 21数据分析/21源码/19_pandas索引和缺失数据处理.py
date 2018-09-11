# coding=utf-8

import pandas as pd
import numpy as np

df = pd.read_csv('dogNames2.csv')
# print(df)
print(df[(800 < df["Count_AnimalName"])&(df["Count_AnimalName"]<1000)])
print(df[(df["Row_Labels"].str.len() > 4)&(df["Count_AnimalName"]>700)])

# NAN处理
t = pd.DataFrame(np.arange(12).reshape((3, 4)), columns=list("WXYZ"))
# print(t)
t.iloc[1:,:2] = np.nan
print(t)
print(pd.isnull(t))
print(pd.notnull(t))
print(t[pd.notnull(t["W"])])
print(t.dropna(axis=0))
# print(t.dropna(axis=0, how="any"))
# print(t.dropna(axis=0, how="all"))
# print(t.dropna(axis=0, how="any", inplace=True))
print(t.fillna(100))
print(t.fillna(t.mean()))
print(t["X"].fillna(t["X"].mean()))

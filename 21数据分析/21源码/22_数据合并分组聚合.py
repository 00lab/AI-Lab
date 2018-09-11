# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt

# 数据的合并
#pd.join();.merge(t2, on="A", how="inner"/"outer"/"left"/"right")

# 分组
file_path = "./starbucks_store_worldwide.csv"
df = pd.read_csv(file_path)
print(df.head(1))
# print(df.info())
grouped = df.groupby(by="Country")
print(grouped)  # DataFrameGroupBy

# 进行遍历
# for i,j in grouped:
#     print(i)
#     print("-"*80)
#     print(j)
#     print("*"*100)
# df[df["Country"]="US"]
# 调用聚合方法
country_count = grouped["Brand"].count()
print(country_count["US"])
print(country_count["CN"])

# 统计中国每个省份的数量
china_data = df[df["Country"] == "CN"]
grouped = china_data.groupby(by="State/Province")
print(grouped["Brand"].count())

# 数据按照多个条件分组
grouped = df["Brand"].groupby(by=[df["Country"], df["State/Province"]]).count()
print(grouped)
print(type(grouped))
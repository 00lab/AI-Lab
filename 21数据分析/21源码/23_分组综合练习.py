# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")  # /usr/share/fonts/truetype/arphic/ukai.ttc")

# 分组
file_path = "./starbucks_store_worldwide.csv"
df = pd.read_csv(file_path)
print(df.head(1))

# 使用matplotlib呈现店铺总数排名前10的国家
# 准备数据
data1 = df.groupby(by="Country").count()["Brand"].sort_values(ascending=False)[:10]
print(data1)
_x = data1.index
_y = data1.values

#plt.figure(figsize=(20, 8), dpi=80)

#plt.bar(range(len(_x)), _y)

#plt.xticks(range(len(_x)), _x)
# plt.show()

df = df[df["Country"] == "CN"]
#print(df.head(1))
data2 = df.groupby(by="City").count()["Brand"].sort_values(ascending=False)[:25]
_x = data2.index
_y = data2.values

plt.figure(figsize=(20, 8), dpi=80)

plt.bar(range(len(_x)), _y, width=0.3)

plt.xticks(range(len(_x)), _x, fontproperties=my_font)
plt.show()
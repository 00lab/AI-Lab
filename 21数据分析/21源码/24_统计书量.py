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
file_path = "./books.csv"
df = pd.read_csv(file_path)
print(df.head(1))
# 统计不同年份书量
data1 = df[pd.notnull(df["original_publication_year"])]
# print(data1.groupby(by="original_publication_year").count()["title"])

# 统计不同年份书的平均评分情况

grouped = data1["average_rating"].groupby(by=data1["original_publication_year"]).mean()
#print(data1["average_rating"].groupby(by=data1["original_publication_year"]).count())
print(grouped)

_x = grouped.index
_y = grouped.values

plt.figure(figsize=(20, 8), dpi=80)
plt.plot(range(len(_x)), _y)
plt.xticks(list(range(len(_x)))[::10], _x[::10].astype(int), rotation=45)
plt.show()
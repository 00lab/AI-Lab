# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt
# from matplotlib import font_manager

# my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")  # /usr/share/fonts/truetype/arphic/ukai.ttc")

file_path = "./911.csv"
df = pd.read_csv(file_path)
# print(df.head(1))

df["timeStamp"] = pd.to_datetime((df["timeStamp"]))
df.set_index("timeStamp", inplace=True)
# print(df.head(5))
count_by_month = df.resample("M").count()["title"]
# print(count_by_month)

_x = count_by_month.index
_y = count_by_month.values

for i in _x:  # 查看有哪些可用方法
    print(dir(i))
    break;

_x = [i.strftime("%Y%m%d") for i in _x]

plt.figure(figsize=(20, 8), dpi=80)
plt.plot(range(len(_x)), _y)
plt.xticks(range(len(_x)), _x, rotation=45)
plt.show()


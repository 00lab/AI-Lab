# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt
# from matplotlib import font_manager

# my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")  # /usr/share/fonts/truetype/arphic/ukai.ttc")

file_path = "./BeijingPM20100101_20151231.csv"
df = pd.read_csv(file_path)
print(df.head(1))

# 把分开的时间字段合并成pandas时间类型
period = pd.PeriodIndex(year=df["year"],month=df["month"], day=df["day"],hour=df["hour"], freq="H")
# print(period)
# print(type(period))
df["datetime"] = period
print(df.head(5))

df.set_index("datetime", inplace=True)
df = df.resample("7D").mean()
# 删除缺失数据
# print(df["PM_US Post"])
data = df["PM_US Post"].dropna()
data_china = df["PM_Dongsi"]

# 画图
_x = data.index
_x = [i.strftime("%Y-%m-%d") for i in _x]
_x_china = [i.strftime("%Y-%m-%d") for i in data_china.index]
_y = data.values
_y_china = data_china.values

plt.figure(figsize=(20, 8), dpi=80)
plt.plot(range(len(_x)), _y, label="US_POST")
plt.plot(range(len(_x)), _y_china, label="CN_POST")
plt.xticks(range(len(_x))[::5], _x[::5], rotation=90)
plt.legend(loc="best")
plt.grid(alpha=0.4, linestyle=":")
plt.show()


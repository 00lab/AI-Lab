# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")  # /usr/share/fonts/truetype/arphic/ukai.ttc")

file_path = "./911.csv"
df = pd.read_csv(file_path)
print(df.head(1))

# 获取分类
# print(df["title"].str.split(": "))
tmp_list = df["title"].str.split(": ").tolist()
cate_list = list(set([i[0] for i in tmp_list]))
print(cate_list)

zeros_df = pd.DataFrame(np.zeros((df.shape[0], len(cate_list))), columns=cate_list)

print(df["title"].str.contains("EMS"))
for cate in cate_list:
    zeros_df[cate][df["title"].str.contains(cate)] = 1

print(zeros_df)

print(zeros_df.sum(axis=0))

cate_list2 = [i[0] for i in tmp_list]
# print(cate_list2)
df["cate"] = pd.DataFrame(np.array(cate_list2).reshape((df.shape[0], 1)), columns=["cate"])
# print(df.head(5))
print(df.groupby(by="cate").count()["title"])
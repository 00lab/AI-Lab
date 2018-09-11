# coding=utf-8

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt

df = pd.read_csv('IMDB-Movie-Data.csv')
print(df.head())
# print(df.info())
print(df["Rating"].mean())
print(len(set(df["Director"].tolist())))
print(len(df["Director"].unique()))

tmp_actor_list = df["Actors"].str.split(", ").tolist()
actor_list = [i for j in tmp_actor_list for i in j]
# actor_list = np.array(tmp_actor_list).flatten()  # 展开

print(len(set(actor_list)))

temp_list = df["Genre"].str.split(",").tolist()
genre_list = list(set([i for j in temp_list for i in j]))
#构造全0数组
zeros_df = pd.DataFrame(np.zeros((df.shape[0], len(genre_list))), columns=genre_list)
# print(zeros_df.head(3))
print(df["Genre"].head(3))
for i in range(df.shape[0]):
    zeros_df.loc[i, temp_list[i]] = 1
print(zeros_df.head(3))
genre_count = zeros_df.sum(axis=0)
print(genre_count)
#排序
genre_count = genre_count.sort_values()
_x = genre_count.index
_y = genre_count.values
print(_y)
plt.figure(figsize=(20, 8), dpi=80)
plt.barh(range(len(_x)), _y)
plt.yticks(range(len(_x)), _x)
plt.show()
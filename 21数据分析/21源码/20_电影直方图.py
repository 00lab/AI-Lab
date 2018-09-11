# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_csv('IMDB-Movie-Data.csv')
print(df.head())
print(df.info())
# df['Revenue (Millions)'] = df['Revenue (Millions)'].fillna(df['Revenue (Millions)'].mean())

runtime_data = df.dropna(axis=0)['Revenue (Millions)'].values
runtime_data[runtime_data > 220] = 220
# runtime_data[runtime_data < 5] = 5

# print(runtime_data)

max_runtime = runtime_data.max()
min_runtime = runtime_data.min()

print(max_runtime)
print(min_runtime)
print((max_runtime - min_runtime))
num_bin = (max_runtime - min_runtime) // 5

plt.figure(figsize=(20,8), dpi=80)
plt.hist(runtime_data, num_bin)

plt.xticks(range(int(min_runtime), int(max_runtime)+5, 5))

plt.show()

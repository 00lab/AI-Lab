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
print(df.head(1))

df["timeStamp"] = pd.to_datetime((df["timeStamp"]))

tmp_list = df["title"].str.split(": ").tolist()
cate_list2 = [i[0] for i in tmp_list]
# print(cate_list2)
df["cate"] = pd.DataFrame(np.array(cate_list2).reshape((df.shape[0], 1)))
print(df.head(2))

df.set_index("timeStamp", inplace=True)
# print(df.head(5))

plt.figure(figsize=(20, 8), dpi=80)

for group_name,group_data in df.groupby(by="cate"):
    # 对不同的类型进行绘图
    count_by_month = group_data.resample("M").count()["title"]
    _x = count_by_month.index
    _y = count_by_month.values
    _x = [i.strftime("%Y%m%d") for i in _x]
    plt.plot(range(len(_x)), _y, label=group_name)


plt.xticks(range(len(_x)), _x, rotation=45)
plt.legend(loc="best")
plt.show()

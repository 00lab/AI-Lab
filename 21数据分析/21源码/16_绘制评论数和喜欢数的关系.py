# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import numpy as np
from matplotlib import pyplot as plt

us_file_path = "./youtube_video_data/US_video_data_numbers.csv"
uk_file_path = "./youtube_video_data/GB_video_data_numbers.csv"

t_uk = np.loadtxt(uk_file_path, delimiter=",", dtype="int")
# 因为离散度太高，只选取喜欢数小于15W的数据以更好观察变化关系，最终可拟合一条关系线
t_uk = t_uk[t_uk[:, 1] <= 150000]
t_uk = t_uk[t_uk[:, -1] <= 25000]

t_uk_comments = t_uk[:, -1]
t_uk_like = t_uk[:, 1]

plt.figure(figsize=(20, 8), dpi=80)
plt.scatter(t_uk_like, t_uk_comments)

plt.show()
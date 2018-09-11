# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt

us_file_path = "./youtube_video_data/US_video_data_numbers.csv"
uk_file_path = "./youtube_video_data/GB_video_data_numbers.csv"

t_us = np.loadtxt(us_file_path, delimiter=",", dtype="int")
# print(t2)

# 取评论数据,因为大数字量很少，故忽略，只取比5000少的数据
t_us_comments = t_us[:, -1]
t_us_comments = t_us_comments[t_us_comments <= 5000]
# print(t_us_comments.max(),t_us_comments.min())
d = 50
bin_nums = (t_us_comments.max()-t_us_comments.min())//d

plt.figure(figsize=(20,8),dpi=80)

plt.hist(t_us_comments,bin_nums)
plt.show()
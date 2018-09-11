# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')


import numpy as np
from matplotlib import pyplot as plt

us_file_path = "./youtube_video_data/US_video_data_numbers.csv"
uk_file_path = "./youtube_video_data/GB_video_data_numbers.csv"

t_uk = np.loadtxt(uk_file_path, delimiter=",", dtype="int")
t_us = np.loadtxt(us_file_path, delimiter=",", dtype="int")

zeros_t = np.zeros((t_us.shape[0], 1)).astype("int")
ones_t = np.ones((t_uk.shape[0], 1)).astype("int")

t_us = np.hstack((t_us, zeros_t))
t_uk = np.hstack((t_uk, ones_t))

print(np.vstack((t_uk, t_us)))

print(np.ones((3, 4)))
print(np.zeros((3,4)))
t2 = np.eye(3)
print(t2)
print(np.argmax(t2, axis=0))
print(np.argmin(t2, axis=1))
t2[t2==1] = -1
print(t2)

# 随机数函数
print(np.random.rand(3,4))  # 均匀（随机）分布的3行4列的0-1范围内的浮点数数组
print(np.random.randn(3,4))  # 3行4列标准正态分布数组，浮点数，平均数0，标准差1
print(np.random.randint(10, 20, (2, 3)))  # 10到19的随机整数
print(np.random.uniform(5, 15, (2, 3)))  # 5到14的浮点数，具有均匀分布特性。
# 随机数种子，种子相同，每次运行产生的随机数也相同
np.random.seed(10)
print(np.random.randint(10, 20, (2, 3)))
print(np.random.rand(2,3))

# numpy进行浅拷贝，视图操作
a = np.arange(6).reshape((2, 3))
print(a)
b = a
b[1, 1] = 10
print(a)
c = a[1, :]
print(c)
c[2] = 15
print(a)

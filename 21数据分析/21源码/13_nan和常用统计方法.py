# coding=utf-8
import numpy as np

t = np.arange(12).reshape(3,4).astype(float)
t[2,2]=np.nan
print(t)
print(np.count_nonzero(t))
print(t != t)
print(np.count_nonzero(t != t))
print(np.isnan(t))

t3=np.arange(12).reshape(3,4)
print(np.sum(t3))
print(np.sum(t3, axis=0))
print(np.sum(t3, axis=1))
print(t3.sum())
print(t3.mean(axis=0))
print(np.median(t3, axis=1))
print(t3.max())
print(t3.min(axis=0))
# 极差,最大值于最小值差
print(np.ptp(t3))
print(np.ptp(t3, axis=0))
# 标准差
print(np.std(t3))
print(np.std(t3, axis=0))
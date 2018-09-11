import numpy as np


file_path = "11_readFile.csv"
t1 = np.loadtxt(file_path,delimiter=",",dtype="int")
print(t1)
# 取单行，连续多行，间隔多行
print("*"*100)
print(t1[1])
print(t1[3:])
print(t1[[1,3,4]])
# 取某行所有的列，取某列所有的行
print("*"*100)
print(t1[1,:])
print(t1[3:,:])
print(t1[[1,3,4],:])
print(t1[:,1])
# 取连续多列，取不连续多列
print("*"*100)
print(t1[:,3:])
print(t1[:,[0,2]])
# 取某行某列的值
a = t1[2, 3]
print(a)
print(type(a))
# 取第3行到第5行，第2列到第4列， 取的是交叉点
b = t1[2:5, 1:4]
print(b)
# 取多个不相邻的点, [0,2],[2,0],[1,3]
c = t1[[0,2,1],[2,0,3]]
print(c)

# 判断小于某个值
print(t1<10)
t2 = t1
t2[t2<10]=3
print(t2)
print(t2[t2>100])
print(np.where(t2<30,0,50))
t2 = t2.astype(float)
t2[3,3] = np.nan
print(t2.clip(10,30))
print(np.nan != np.nan)
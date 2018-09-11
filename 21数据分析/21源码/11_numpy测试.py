import numpy as np
import random

a = np.array([1,2,3])
b = np.array(range(6))
c = np.array(range(9), dtype=float)
d = np.array(range(9), dtype="i1")

print(a)
print(a.dtype)
print(b)
print(type(b))
print(c)
print(c.dtype)
print(d)
print(d.dtype)

t5 = np.array([1,1,0,1,0,0], dtype=bool)
print(t5)
print(t5.dtype)

# 调整数据类型
t6 = t5.astype("int8")
print(t6)
print(t6.dtype)

t7 = np.array([random.random() for i in range(10)])
print(t7)
print(t7.dtype)
# 取小数点后两位
t8 = np.round(t7, 2)
print(t8)
print(round(random.random(), 3))
print("%.2f"%random.random())

# 矩阵的shape
print(a.shape)
ts = np.array([[1,2,3],[4,5,6]])
print(ts)
print(ts.shape)
# print(ts.reshape((3,4))) # 报错，没有那么多元素
print(ts.reshape((3,2)))
print(ts.reshape((1,6)))
print(ts.reshape((6,1)))
print(ts.reshape((6,)))
print(ts.reshape(ts.shape[0]*ts.shape[1]))
# 矩阵的运算
# 与数字运算
t_calcu = np.array([[0,1,2,3],[4,5,6,7]])
print(t_calcu*2)
print(t_calcu+2)
print(t_calcu/2)
# print(t_calcu/0)  # 不报错，只是警告，0/0结果非数字nan，数字/0结果无穷inf
# 与矩阵运算
tc2 = np.array([[1,2,3,4],[5,6,7,8]])
print(tc2-t_calcu)
tc3 = np.array([1,2,3,4])
print(tc3-t_calcu)
# tc4 = np.array([[1],[2]])
tc4 = np.arange(1,3).reshape((2,1))
print("tc4-t_calcu:")
print(tc4-t_calcu)

# 读取本地文本文件
file_path = "11_readFile.csv"
t_read_file = np.loadtxt(file_path,delimiter=",",dtype="int")
t_read_file2 = np.loadtxt(file_path,delimiter=",",dtype="int",unpack=True)  # 矩阵转置
print(t_read_file)
print(t_read_file2)
# 矩阵转置
print(t_read_file.transpose())
print(t_read_file.T)
print(t_read_file.swapaxes(1,0))  # 转换1和0轴

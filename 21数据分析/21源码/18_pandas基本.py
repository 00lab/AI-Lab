# coding=utf-8

import pandas as pd
import numpy as np

print(pd.Series([1,2,3,4,5]))
print(type(pd.Series([1,2,3,4,5])))
print(pd.Series([1,2,3,4,5], index=list("abcde")))
tmp_dict = {"name":"xiaohong", "age":30, "tel":10086}
print(pd.Series(tmp_dict))
t1 = pd.Series([1,2,3,4,5])
print(t1.dtype)
print(t1.astype(float))
t2 = pd.Series(tmp_dict)
print(t2["age"])
print(t2[2])
print(t2[:2])
print(t2[["age", "tel"]])
print(t2.index)
print(type(t2.index))
print(t2.values)
print(type(t2.values))

# 读文件
df = pd.read_csv('dogNames2.csv')
print(df)

# 建立data frame
print(pd.DataFrame(np.arange(12).reshape((3, 4)), index=list("abc"), columns=list("WXYZ")))
d1 = {"name":["xm","xg"],"age":[23,56],"tel":[10086,10010]}
print(pd.DataFrame(d1))
d2 = [{"name":"xw","age":23,"tel":10232},{"name":"xg","tel":23124},{"name":"xm","age":32}]
print(pd.DataFrame(d2))


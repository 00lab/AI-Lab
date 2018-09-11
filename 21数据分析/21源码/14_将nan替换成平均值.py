# coding=utf-8
import numpy as np


def fill_ndarray(t):
    for i in range(t.shape[1]):
        temp_col = t[:,i]
        nan_num = np.count_nonzero(temp_col!=temp_col)
        if nan_num != 0:  # 不为0，说明当前列有nan
            temp_not_nan_col = temp_col[temp_col==temp_col]  # 获得当前列所有不为nan的值够成的array
            # 选中nan的位置，并重新赋值成均值
            temp_col[np.isnan(temp_col)] = temp_not_nan_col.mean()
    return t


if __name__ == '__main__':
    t = np.arange(24).reshape(4, 6).astype(float)
    t[2, 2:] = np.nan
    print(t)
    t = fill_ndarray(t)
    print(t)

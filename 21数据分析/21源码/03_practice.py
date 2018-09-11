# coding utf-8

from matplotlib import pyplot as plt
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")

x = range(11,31)
y = [1,0,1,1, 2,4,3,2, 3,4,4,5, 6,5,4,3, 3,1,1,1]

plt.figure(figsize=(10,8), dpi=80)

_x = list(x)
_xtick_lables = ["{}岁".format(i) for i in _x]
plt.xticks(_x, _xtick_lables, rotation=315, fontproperties=my_font)
plt.yticks(range(0,9))
plt.grid(alpha=0.4)
plt.xlabel("年龄", fontproperties=my_font)
plt.ylabel("数量 单位(个)", fontproperties=my_font)
plt.title("11岁到30岁对象个数统计", fontproperties=my_font)

plt.plot(x, y)
plt.show()
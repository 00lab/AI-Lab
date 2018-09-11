#coding=utf-8

from matplotlib import pyplot as plt
import random
import matplotlib
from matplotlib import font_manager

# windows和linux设置字体的方法
# font = {'family': 'MicroSoft YaHei',
#         'weight': 'bold',
#         'size': 'larger'}
#
# matplotlib.rc("font", **font)

# 另外一种设置字体的方式
# fc-list查看linux下所有的字体，fc-list :lang=zh查看所有中文字体
my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/uming.ttc")

x=range(0, 120)
y=[random.randint(20,35) for i in range(120)]

plt.figure(figsize=(20,8),dpi=60)

# 调整x轴的刻度
_x = list(x)
_xtick_lables = ["10点{}分".format(i) for i in range(60)]
_xtick_lables += ["11点{}分".format(i) for i in range(60)]
plt.xticks(_x[::3], _xtick_lables[::3],rotation=315,fontproperties=my_font)  # rotation是旋转的度数

# 添加描述信息
plt.xlabel("时间", fontproperties=my_font)
plt.ylabel("温度 单位(℃)", fontproperties=my_font)
plt.title("10点到12点每分钟温度变化统计", fontproperties=my_font)

plt.plot(x, y)
plt.show()
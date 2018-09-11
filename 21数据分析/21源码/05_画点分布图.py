from matplotlib import pyplot as plt
from matplotlib import font_manager


my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
a = [11,17,16,11,12,11,12,6, 6, 7, 8, 9, 12,15,14,17,18,21,16,17,20,14,15,15,15,19,21,22,22,22,23]
b = [26,26,28,19,21,17,16,19,18,20,20,19,22,23,17,20,21,20,22,15,11,15,5,13,17,10,11,13,12,13, 6]

x_3 = range(1, 32)
x_10 = range(51, 82)

plt.figure(figsize=(30, 8), dpi=80)

plt.scatter(x_3, a, label='3月份')
plt.scatter(x_10, b, label='10月份')

_x = list(x_3) + list(x_10)
_xtick_labels = ["3月{}日".format(i) for i in x_3]
_xtick_labels += ["10月{}日".format(i) for i in x_10]
plt.xticks(_x[::3], _xtick_labels[::3], fontproperties=my_font,rotation=45)

plt.legend(loc="upper left", prop=my_font)

plt.xlabel("时间", fontproperties=my_font)
plt.ylabel("温度", fontproperties=my_font)

plt.show()
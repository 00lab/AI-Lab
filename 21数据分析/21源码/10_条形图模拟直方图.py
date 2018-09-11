from matplotlib import pyplot as plt
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")

interval = [0,5,10,15,20,25,30,35,40,45,60,90]
wictth = [5,5,5,5,5,5,5,5,5,15,30,60]
quantity = [836,2737,3723,3926,3596,1438,3273,642,824,613,215,47]

plt.bar(range(len(quantity)), quantity, width=1)

_x = [i-0.5 for i in range(len(interval)+1)]
_xtick_labels = interval+[(interval[-1]+wictth[-1])]

plt.xticks(_x, _xtick_labels)

plt.show()
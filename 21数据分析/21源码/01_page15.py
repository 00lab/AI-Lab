
from matplotlib import pyplot as plt

x = range(2, 26, 2)
y = [15,13,14,5,17,20,25,26,26,27,22,18]

# 设置图片大小
plt.figure(figsize=(10,8), dpi=80)
plt.plot(x,y)

plt.xticks(range(2,24))  # 绘制x
# plt.savefig("./test.png")  # 保存
plt.show()

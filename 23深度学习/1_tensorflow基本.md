# tensorflow基本

从下面这个最简单的程序开始学习tensorflow。

``` python
import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 将警告等级设为2

# 实现一个加法运算
def add_test():
    a = tf.constant(5.0)  # 定义一个常数
    b = tf.constant(6.0)
    sum1 = tf.add(a, b)  # 累加
    print(a, b, sum1)

    with tf.Session() as sess:  # 创建一个会话
        print(sess.run(sum1))


if __name__ == '__main__':
    add_test()
    
```

输出：

```
Tensor("Const:0", shape=(), dtype=float32) Tensor("Const_1:0", shape=(), dtype=float32) Tensor("Add:0", shape=(), dtype=float32)
11.0
```

上面那个程序从上到下开始读：
1. 导入包

   版本说明：tensorflow：1.10.1，numpy：1.14.5，

2. os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 以防止警告

   <font color="#dd0000">I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: FMA</font>

3. 定义常量a = tf.constant(5.0)，返回的a是一个“张量”（Tensor），至于张量其实就是新定义的一种数据类型而已，所以会打印出Tensor("Const:0", shape=(), dtype=float32)属性。

4. 要打印出结果信息则需要开启个会话（Session）。

5. 张量、会话等将在后面详细介绍。


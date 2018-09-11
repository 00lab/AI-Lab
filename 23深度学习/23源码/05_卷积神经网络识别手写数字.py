import tensorflow as tf
import os
from tensorflow.examples.tutorials.mnist import input_data


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 将警告等级设为2


def full_connected():
    # 获取真实数据
    mnist = input_data.read_data_sets("./data/mnist/input_data/", one_hot=True)

    # 1.建立数据的占位符 x [None, 784], y_true [None, 10]
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])
        y_true = tf.placeholder(tf.int32, [None, 10])
    # 2.建立一个全连接层的神经网络， w[784, 10] b[10]
    with tf.variable_scope("fc_model"):
        # 随机初始化权重和偏置
        weight = tf.Variable(tf.random_normal([784, 10], mean=0.0, stddev=1.0), name="w")
        bias = tf.Variable(tf.constant(0.0, shape=[10]))
        # 预测None个样本的输出结果matrix[None, 784]*[784, 10] + [10] = [None, 10]
        y_predict = tf.matmul(x, weight) + bias
    # 3.求出所有样本的损失，然后求平均值
    with tf.variable_scope("soft_cross"):
        # 求平均交叉熵损失
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))
    # 4.梯度下降求出损失
    with tf.variable_scope("optimizer"):
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
    # 5.计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
        # equal_list None个样本 [1,0,1,0,0,1,1,1,........]
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 定义个初始化变量的op
    init_op = tf.global_variables_initializer()

    # 收集变量，单个数字值收集
    tf.summary.scalar("losses", loss)
    tf.summary.scalar("acc", accuracy)
    #高纬度变量收集
    tf.summary.histogram("weightes", weight)
    tf.summary.histogram("biases", bias)
    # 定义一个合并变量op
    merged = tf.summary.merge_all()

    #开启会话训练
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 建立events文件，然后写入
        file_writer = tf.summary.FileWriter("./tmp/summary/", graph=sess.graph)

        # 迭代训练，更新参数预测
        for i in range(2000):
            # 取出真实存在的特征值和目标值
            mnist_x, mnist_y = mnist.train.next_batch(50)

            # 运行train_op训练
            sess.run(train_op, feed_dict={x:mnist_x, y_true:mnist_y})

            # 写入每步训练的值
            summary = sess.run(merged, feed_dict={x:mnist_x, y_true:mnist_y})
            file_writer.add_summary(summary, i)

            print("训练第%d步，准确率：%f" % (i, sess.run(accuracy, feed_dict={x:mnist_x, y_true:mnist_y})))


def model():
    """
    自定义卷积模型
    :return:
    """
    # 1.准备数据占位符 x[None, 784] y_true[None, 10]
    # 1.建立数据的占位符 x [None, 784], y_true [None, 10]
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])
        y_true = tf.placeholder(tf.int32, [None, 10])
    # 2.一卷积层 卷积：5*5*1， 32个， strides=1, 激活：tf.relu，池化
    with tf.variable_scope("cnnv1"):
        # 初始化权重, 偏置[32]
        shape_w = [5, 5, 1, 32]
        w_cnn1 = tf.Variable(tf.random_normal(shape=shape_w, mean=0.0, stddev=1.0))
        shape_b = [32]
        b_cnn1 = tf.Variable(tf.constant(0.0, shape=shape_b))
        # 对x改变形状 x[None, 784] -> [None, 28, 28, 1]
        x_reshape = tf.reshape(x, [-1, 28, 28, 1])
        # [None, 28, 28, 1] -> [None, 28, 28, 32]
        x_relu1 = tf.nn.relu(tf.nn.conv2d(x_reshape, w_cnn1, strides=[1, 1, 1, 1], padding="SAME") + b_cnn1)
        # 池化 2*2， strides 2 [None, 28, 28, 32] -> [None, 14, 14, 32]
        x_pool1 = tf.nn.max_pool(x_relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    # 3.二卷积层,卷积：5*5*32， 64个filter， strides=1, 激活：tf.relu，池化
    with tf.variable_scope("cnnv2"):
        # 初始化权重, 权重[5, 5, 32, 64]，偏置[64]
        shape_w = [5, 5, 32, 64]
        w_cnn2 = tf.Variable(tf.random_normal(shape=shape_w, mean=0.0, stddev=1.0))
        shape_b = [64]
        b_cnn2 = tf.Variable(tf.constant(0.0, shape=shape_b))
        # 卷积，激活，池化
        # [None, 14, 14, 32] -> [None, 14, 14, 64]
        x_relu2 = tf.nn.relu(tf.nn.conv2d(x_pool1, w_cnn2, strides=[1, 1, 1, 1], padding="SAME") + b_cnn2)
        # 池化2*2，stride 2, [None, 14, 14, 64] -> [None, 7, 7, 64]
        x_pool2 = tf.nn.max_pool(x_relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    # 4.全连接层 [None, 7, 7, 64] -> [None, 7*7*64]*[7*7*64, 10]+[10] = [None, 10]
    with tf.variable_scope("fc"):
        # 随机初始化权重和偏置
        shape_w = [7*7*64, 10]
        w_fc = tf.Variable(tf.random_normal(shape=shape_w, mean=0.0, stddev=1.0))
        shape_b = [10]
        b_fc = tf.Variable(tf.constant(0.0, shape=shape_b))
        # 修改形状[None, 7, 7, 64] -> [None, 7*7*64]
        x_fc_reshape = tf.reshape(x_pool2, [-1, 7*7*64])
        # 进行矩阵运算得出每个样本的10个结果
        y_predict = tf.matmul(x_fc_reshape, w_fc) + b_fc

    return x, y_true, y_predict



def conv_fc():
    # 获取真实数据
    mnist = input_data.read_data_sets("./data/mnist/input_data/", one_hot=True)
    # 定义模型，得出输出
    x, y_true, y_predict = model()
    # 进行交叉熵损失计算
    # 3.求出所有样本的损失，然后求平均值
    with tf.variable_scope("soft_cross"):
        # 求平均交叉熵损失
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))
    # 4.梯度下降求出损失
    with tf.variable_scope("optimizer"):
        train_op = tf.train.GradientDescentOptimizer(0.0001).minimize(loss)
    # 5.计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
        # equal_list None个样本 [1,0,1,0,0,1,1,1,........]
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 定义个初始化变量的op
    init_op = tf.global_variables_initializer()

    #开启会话训练
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 迭代训练，更新参数预测
        for i in range(2000):
            # 取出真实存在的特征值和目标值
            mnist_x, mnist_y = mnist.train.next_batch(50)

            # 运行train_op训练
            sess.run(train_op, feed_dict={x:mnist_x, y_true:mnist_y})

            print("训练第%d步，准确率：%f" % (i, sess.run(accuracy, feed_dict={x:mnist_x, y_true:mnist_y})))


if __name__ == '__main__':
    conv_fc()
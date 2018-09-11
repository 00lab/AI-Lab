import tensorflow as tf
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 将警告等级设为2


def my_regression():
    """
    自实现一个线性回归预测
    :return: None
    """
    # 1.准备数据， x特征值[100, 1]  y目标值[100]
    x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
    # 矩阵相乘必须是二维
    y_true = tf.matmul(x, [[0.7]]) + 0.8

    # 2. 建立线性回归模型 1个特征，1个权重，一个偏置y = wx + b
    # 随机给一个权重和偏置的值，去计算损失，然后再在当前状态下优化
    # 用变量定义才能优化
    weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="weight", trainable=True)
    bias = tf.Variable(0.0, name="b")
    y_predict = tf.matmul(x, weight) + bias
    # 3. 建立损失函数，均方误差
    loss = tf.reduce_mean(tf.square(y_true - y_predict))
    # 4. 梯度下降优化损失 leaning_rate:0~1,2,3,5,7,10. 学习率大容易梯度爆炸，学习率太小梯度消失
    train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 打印随机初始化的权重和偏重
        print("随机初始化的参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))
        # 循环训练，运行优化
        for i in range(200):
            sess.run(train_op)
            print("优化参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))
    return None


def test_scope():
    """
    线性回归预测，通过作用域让程序模块化，让后台可视化图行显示更加简洁
    :return: None
    """
    with tf.variable_scope("data"):
        # 1.准备数据， x特征值[100, 1]  y目标值[100]
        x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
        # 矩阵相乘必须是二维
        y_true = tf.matmul(x, [[0.7]]) + 0.8
    with tf.variable_scope("model"):
        # 2. 建立线性回归模型 1个特征，1个权重，一个偏置y = wx + b
        # 随机给一个权重和偏置的值，去计算损失，然后再在当前状态下优化
        # 用变量定义才能优化
        weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="weight", trainable=True)
        bias = tf.Variable(0.0, name="b")
        y_predict = tf.matmul(x, weight) + bias
    with tf.variable_scope("loss"):
        # 3. 建立损失函数，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))
    with tf.variable_scope("optimizer"):
        # 4. 梯度下降优化损失 leaning_rate:0~1,2,3,5,7,10. 学习率大容易梯度爆炸，学习率太小梯度消失
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 打印随机初始化的权重和偏重
        print("随机初始化的参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))

        # 建立事件文件
        file_writer = tf.summary.FileWriter("./tmp", graph=sess.graph)

        # 循环训练，运行优化
        for i in range(200):
            sess.run(train_op)
            print("优化参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))
    return None


def test_variable_show():
    """
    线性回归预测，增加变量显示，观察模型参数、损失值等在tensorboard中显示
    1.收集变量，2.合并变量写入事件文件
    :return: None
    """
    with tf.variable_scope("data"):
        # 1.准备数据， x特征值[100, 1]  y目标值[100]
        x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
        # 矩阵相乘必须是二维
        y_true = tf.matmul(x, [[0.7]]) + 0.8
    with tf.variable_scope("model"):
        # 2. 建立线性回归模型 1个特征，1个权重，一个偏置y = wx + b
        # 随机给一个权重和偏置的值，去计算损失，然后再在当前状态下优化
        # 用变量定义才能优化
        weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="weight", trainable=True)
        bias = tf.Variable(0.0, name="b")
        y_predict = tf.matmul(x, weight) + bias
    with tf.variable_scope("loss"):
        # 3. 建立损失函数，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))
    with tf.variable_scope("optimizer"):
        # 4. 梯度下降优化损失 leaning_rate:0~1,2,3,5,7,10. 学习率大容易梯度爆炸，学习率太小梯度消失
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    # 1. 收集tensor
    tf.summary.scalar("losses", loss)
    tf.summary.histogram("weights", weight)
    # 定义合并tensor的op
    merged = tf.summary.merge_all()

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 打印随机初始化的权重和偏重
        print("随机初始化的参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))

        # 建立事件文件
        file_writer = tf.summary.FileWriter("./tmp", graph=sess.graph)

        # 循环训练，运行优化
        for i in range(500):
            sess.run(train_op)

            # 运行合并的tensor
            summary = sess.run(merged)
            file_writer.add_summary(summary, i)

            print("第%d次优化参数 权重：%f, 偏置：%f" % (i, weight.eval(), bias.eval()))
    return None


def test_save_model():
    """
    线性回归预测，模型保存和加载
    :return: None
    """
    with tf.variable_scope("data"):
        # 1.准备数据， x特征值[100, 1]  y目标值[100]
        x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
        # 矩阵相乘必须是二维
        y_true = tf.matmul(x, [[0.7]]) + 0.8
    with tf.variable_scope("model"):
        # 2. 建立线性回归模型 1个特征，1个权重，一个偏置y = wx + b
        # 随机给一个权重和偏置的值，去计算损失，然后再在当前状态下优化
        # 用变量定义才能优化
        weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="weight", trainable=True)
        bias = tf.Variable(0.0, name="b")
        y_predict = tf.matmul(x, weight) + bias
    with tf.variable_scope("loss"):
        # 3. 建立损失函数，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))
    with tf.variable_scope("optimizer"):
        # 4. 梯度下降优化损失 leaning_rate:0~1,2,3,5,7,10. 学习率大容易梯度爆炸，学习率太小梯度消失
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    # 1. 收集tensor
    tf.summary.scalar("losses", loss)
    tf.summary.histogram("weights", weight)
    # 定义合并tensor的op
    merged = tf.summary.merge_all()

    # 定义一个保存模型的实例
    saver = tf.train.Saver()

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 打印随机初始化的权重和偏重
        print("随机初始化的参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))

        # 建立事件文件
        file_writer = tf.summary.FileWriter("./tmp", graph=sess.graph)

        # 加载模型，覆盖模型中随机定义的参数，从上次训练的参数开始
        if os.path.exists("./tmp/ckpt/checkpoint"):
            print("加载模型参数")
            saver.restore(sess, "./tmp/ckpt/model")

        # 循环训练，运行优化
        for i in range(200):
            sess.run(train_op)

            # 运行合并的tensor
            summary = sess.run(merged)
            file_writer.add_summary(summary, i)

            print("第%d次优化参数 权重：%f, 偏置：%f" % (i, weight.eval(), bias.eval()))
        saver.save(sess, "./tmp/ckpt/model")
    return None


def test_terminal_param():
    """
    线性回归预测，定义命令行参数，在运行程序紧跟命令行输入
    python3 02_线性回归练习.py --max_step=150 --model_dir="./tmp/ckpt/model"
    :return: None
    """
    # 定义一个参数：名字，默认值，说明
    tf.app.flags.DEFINE_integer("max_step", 100, "模型训练的步数")
    tf.app.flags.DEFINE_string("model_dir", "./tmp/ckpt/model", "模型文件的加载和保存的路径")
    # 定义获取命令行参数的名字
    FLAGS = tf.app.flags.FLAGS
    with tf.variable_scope("data"):
        # 1.准备数据， x特征值[100, 1]  y目标值[100]
        x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
        # 矩阵相乘必须是二维
        y_true = tf.matmul(x, [[0.7]]) + 0.8
    with tf.variable_scope("model"):
        # 2. 建立线性回归模型 1个特征，1个权重，一个偏置y = wx + b
        # 随机给一个权重和偏置的值，去计算损失，然后再在当前状态下优化
        # 用变量定义才能优化
        weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0), name="weight", trainable=True)
        bias = tf.Variable(0.0, name="b")
        y_predict = tf.matmul(x, weight) + bias
    with tf.variable_scope("loss"):
        # 3. 建立损失函数，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))
    with tf.variable_scope("optimizer"):
        # 4. 梯度下降优化损失 leaning_rate:0~1,2,3,5,7,10. 学习率大容易梯度爆炸，学习率太小梯度消失
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    # 1. 收集tensor
    tf.summary.scalar("losses", loss)
    tf.summary.histogram("weights", weight)
    # 定义合并tensor的op
    merged = tf.summary.merge_all()

    # 定义一个保存模型的实例
    saver = tf.train.Saver()

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 打印随机初始化的权重和偏重
        print("随机初始化的参数 权重：%f, 偏置：%f" % (weight.eval(), bias.eval()))

        # 建立事件文件
        file_writer = tf.summary.FileWriter("./tmp", graph=sess.graph)

        # 加载模型，覆盖模型中随机定义的参数，从上次训练的参数开始
        if os.path.exists("./tmp/ckpt/checkpoint"):
            print("加载模型参数")
            saver.restore(sess, FLAGS.model_dir)

        # 循环训练，运行优化
        for i in range(FLAGS.max_step):
            sess.run(train_op)

            # 运行合并的tensor
            summary = sess.run(merged)
            file_writer.add_summary(summary, i)

            print("第%d次优化参数 权重：%f, 偏置：%f" % (i, weight.eval(), bias.eval()))
        saver.save(sess, FLAGS.model_dir)
    return None


if __name__ == '__main__':
    # my_regression()
    # test_scope()
    # test_variable_show()
    # test_save_model()
    test_terminal_param()

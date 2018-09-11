import tensorflow as tf
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 将警告等级设为2


# 实现一个加法运算
def add_test():
    a = tf.constant(5.0)
    b = tf.constant(6.0)
    sum1 = tf.add(a, b)
    print(a, b, sum1)

    with tf.Session() as sess:
        print(sess.run(sum1))


def show_graph():
    """
    查看tf图：默认定义一张图，相当于给程序分配内存
    :return: None
    """
    a = tf.constant(5.0)
    b = tf.constant(6.0)
    sum1 = tf.add(a, b)
    graph = tf.get_default_graph()
    print(graph)

    # 创建一张图，上下文环境
    g = tf.Graph()
    with g.as_default():
        c = tf.constant(1.0)
        print(c.graph)
    # op:只要用tensorflow的API定义的都是op，相当于载体， tensor：就指代数据。由op承载。
    #with tf.Session(graph=g) as sess:
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
        print(sess.run(sum1))
        print(a.graph)
        print(sum1.graph)
        print(sess.graph)
    # 会话：1 运行图结构，2 分配资源计算，3 掌握资源（变量的资源、队列、线程等）


def test_placeholder():
    """
    实时训练时用，placeholder是一个占位符，feed_dict是一个字典
    :return: None
    """
    # plt = tf.placeholder(tf.float32, [2, 3])
    plt = tf.placeholder(tf.float32, [None, 3])
    print(plt)
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
        print(sess.run(plt, feed_dict={plt:[[1, 2, 3], [4, 5, 6]]}))


def shape_test():
    """
    形状的概念：静态形状、动态形状
    :return: None
    """
    plt = tf.placeholder(tf.float32, [None, 2])
    print(plt)
    plt.set_shape([3, 2])
    print(plt)
    # plt.set_shape([4, 2])  # 错误，静态形状一旦张量形状固定，不能再次设置静态形状。不能夸维修改，1D->1D,2D->2D
    plt_reshape = tf.reshape(plt, [2, 3])  # 动态形状可创建一新张量，改变时一定要注意元素数量匹配，1D->3D
    print(plt_reshape)
    with tf.Session() as sess:
        pass


def api_test():
    """
    产生全为0\1等数组
    :return: None
    """
    zero = tf.zeros([3, 4], tf.float32)
    print(zero)
    one = tf.ones([3, 4], tf.float32)
    print(one)
    a = tf.cast([[1, 2], [3, 4]], tf.float32)
    print(a)
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8, 9], [10, 11, 12]]
    c = tf.concat([a, b], axis=0)
    # c = tf.concat([a, b], axis=1)
    print(c)
    with tf.Session() as sess:
        # print(sess.run([zero, one]))
        print(sess.run(zero))
        print(sess.run(one))
        print(sess.run(c))


def test_variable():
    """
    变量
    1. 变量op能够持久保存，普通张量op不行。
    2. 当定义一个变量op时，必须在会话中运行初始化
    3. name参数：在tensorboard使用时显示名字，可让相同op名字进行区分
    :return:None
    """
    a = tf.constant([1, 2, 3, 4])
    var = tf.Variable(tf.random_normal([2, 3], mean=0.0, stddev=1.0))
    print(a, var)
    # 必须显示初始化变量op
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        # 必须运行初始化op
        sess.run(init_op)
        print(sess.run([a, var]))


def tensorboard_test():
    """
    可视化图结构测试
    :return: None
    """
    # a = tf.constant([1, 2, 3, 4])
    a = tf.constant(3.0, name="a")
    b = tf.constant(4.0, name="b")
    c = tf.add(a, b)
    var = tf.Variable(tf.random_normal([2, 3], mean=0.0, stddev=1.0), name="var")
    print(a, var)
    # 必须显示初始化变量op
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        # 必须运行初始化op
        sess.run(init_op)
        print(sess.run([c, var]))
        # 把程序的图结构写入事件文件，graph:把指定的图写进事件文件中
        file_witer = tf.summary.FileWriter("./tmp", graph=sess.graph)


if __name__ == '__main__':
    # add_test()
    # show_graph()
    # test_placeholder()
    # shape_test()
    # api_test()
    # test_variable()
    tensorboard_test()

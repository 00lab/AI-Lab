import tensorflow as tf
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 将警告等级设为2


def test_queue():
    """
    模拟同步处理数据，将数据存如queue
    :return: None
    """
    # 1.定义队列
    q = tf.FIFOQueue(3, tf.float32)
    # 放入数据
    enq_many = q.enqueue_many([[0.2, 0.2, 0.3],])
    # 2.定义读取数据过程  取数据+1，入队列
    out_q = q.dequeue()
    data = out_q + 1
    en_q = q.enqueue(data)
    with tf.Session() as sess:
        # 初始化队列
        sess.run(enq_many)
        # 处理数据
        for i in range(100):
            sess.run(en_q)
        # 训练数据
        for i in range(q.size().eval()):
            print(sess.run(q.dequeue()))


def test_muti_thread_queue():
    """
    模拟多线程读取数据并处理数据
    :return: None
    """
    # 1.定义队列， 1000
    q = tf.FIFOQueue(3, tf.float32)
    # 2.循环值 +1，入队列
    var = tf.Variable(0.0)
    # 实现自增 tf.assign_add
    data = tf.assign_add(var, tf.constant(1.0))

    en_q = q.enqueue(data)
    # 3.定义队列管理op,指定多少个子线程，子线程该做什么事
    qr = tf.train.QueueRunner(q, enqueue_ops=[en_q]*2)
    # 初始化变量op
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)
        # 开启线程管理器
        coord = tf.train.Coordinator()
        # 开启子线程
        threads = qr.create_threads(sess, coord=coord, start=True)
        # 主线程， 不断读取数据训练
        for i in range(300):
            print(sess.run(q.dequeue()))
        # 回收
        coord.request_stop()
        coord.join(threads)


def csv_read(filelist):
    """
    读取csv文件
    :param filelist:文件路径+名字的列表
    :return:读取的内容
    """
    # 1.构造文件队列
    file_queue = tf.train.string_input_producer(filelist)
    # 2.构造csv阅读器读取队列数据（按一行）
    reader = tf.TextLineReader()
    key, value = reader.read(file_queue)
    # print(value)
    # 3.对每行内容解码
    # 参数record_defaults 指定每个样本的每列的类型，以及指定默认值。[["None],[4]]
    records = [["None"], ["None"]]
    example, label = tf.decode_csv(value, record_defaults=records)
    # 第一列， 第二列
    # return example, label

    # 4.默认只读一行，想要读取多个数据需要批处理
    example_batch, label_batch = tf.train.batch([example, label], batch_size=20, num_threads=1, capacity=9)
    return example_batch, label_batch


def csv_read_manager():
    """
    找到文件，读取内容
    :return: None
    """
    # 找到文件，放入列表  路径+名字 -> 列表
    file_name = os.listdir("./data/csvdata/")
    file_list = [os.path.join("./data/csvdata/", file) for file in file_name]
    # print(file_list)
    # example, label = csv_read(file_list)
    example_batch, label_batch = csv_read(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启读文件线程
        threads = tf.train.start_queue_runners(sess, coord=coord)
        # 打印读取的内容, 默认只读一行
        # print(sess.run([example, label]))
        print(sess.run([example_batch, label_batch]))
        # 回收子线程
        coord.request_stop()
        coord.join(threads)


def imgread(filelist):
    """
    读取图片并转换成张量
    :param filelist:文件路劲+名字列表
    :return: 每张图片的张量
    """
    # 1.构造文件队列
    file_queue = tf.train.string_input_producer(filelist)
    # 2.构造阅读器读取图片内容，默认读取一张图
    reader = tf.WholeFileReader()
    key, value = reader.read(file_queue)
    # 3.对读取的图片数据进行解码
    # img = tf.image.decode_png(value)
    img = tf.image.decode_jpeg(value)
    print(img)
    # 5.处理图片的大小， 统一大小
    img_resize = tf.image.resize_images(img, [100, 100])
    print(img_resize)
    # 注意：一定要把样本的形状固定[100, 100, 3],在批处理时要求所有数据形状固定
    img_resize.set_shape([100, 100, 3])
    print(img_resize)
    # 6.进行批处理
    img_batch = tf.train.batch([img_resize], batch_size=5, num_threads=1, capacity=5)
    print(img_batch)
    return img_batch


def img_read_manager():
    """
    找到文件，读取内容
    :return: None
    """
    # 找到文件，放入列表  路径+名字 -> 列表
    file_name = os.listdir("./data/imgdata/")
    file_list = [os.path.join("./data/imgdata/", file) for file in file_name]
    print(file_list)

    img_batch = imgread(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启读文件线程
        threads = tf.train.start_queue_runners(sess, coord=coord)
        # 打印读取的内容
        print(sess.run([img_batch]))
        # 回收子线程
        coord.request_stop()
        coord.join(threads)


class CifarRead(object):
    """
    完成读取二进制文件，写进tfrecords,读取tfrecords
    """
    def __init__(self, filelist):
        self.file_list = filelist
        # 定义读取的图片的属性
        self.height = 32
        self.width = 32
        self.channel = 3
        # 二进制文件每张图片的字节
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.label_bytes + self.image_bytes

    def read_and_decode(self):
        # 1.构造文件队列
        file_queue = tf.train.string_input_producer(self.file_list)
        # 2.构造二进制文件读取器，读取内容
        reader = tf.FixedLengthRecordReader(self.bytes)
        key, value = reader.read(file_queue)
        print(value)
        # 3.解码内容
        label_img = tf.decode_raw(value, tf.uint8)
        print(label_img)
        # 4.分割出图片和标签数据，特征值和目标值
        label = tf.cast(tf.slice(label_img, [0], [self.label_bytes]), tf.int32)
        img = tf.slice(label_img, [self.label_bytes], [self.image_bytes])
        print(label, img)
        # 5.对图片的特征数据进行形状改变,[3072] -> [32, 32, 3]
        img_reshape = tf.reshape(img, [self.height, self.width, self.channel])
        print(label, img_reshape)
        # 6.批处理数据
        img_batch, label_batch = tf.train.batch([img_reshape,label], batch_size=10, num_threads=1, capacity=10)
        print(img_batch, label_batch)
        return img_batch,label_batch

    def write_to_tfrecords(self, file_path, image_batch, label_batch):
        """
        将图片的特征值和目标值存进tfrecords
        :param image_batch: 10张图片的特征值
        :param label_batch: 10张图片的目标值
        :return: None
        """
        # 1.建立TFRecord存储器
        writer = tf.python_io.TFRecordWriter(file_path)
        # 2.循环将所有样本写入文件，每张图片样本都需要构造example协议
        for i in range(10):
            # 取出第i个图片数据的特征值和目标值
            image = image_batch[i].eval().tostring()
            label = label_batch[i].eval()[0]
            # 构造一个样本example
            example = tf.train.Example(features=tf.train.Features(feature={
                "image":tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
                "label":tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
            }))
            # 写入单个样本
            writer.write(example.SerializeToString())
        #关闭
        writer.close()

    def read_from_tfrecords(self, file_path):
        """
        读取tfrecords文件
        :param file_path:
        :return:
        """
        # 1.构造文件队列
        file_queue = tf.train.string_input_producer([file_path])
        # 2.构造文件阅读器，读取内容example,value，一个样本的序列化example
        reader = tf.TFRecordReader()
        key, value = reader.read(file_queue)
        # 3.解析example
        features = tf.parse_single_example(value, features={
            "image":tf.FixedLenFeature([], tf.string),
            "label":tf.FixedLenFeature([], tf.int64)
        })
        # print(features["image"], features["label"])
        # 4.解码内容，如果读取的内容格式是string需要解码，如果是int64,float32不需要解码
        image = tf.decode_raw(features["image"], tf.uint8)
        label = tf.cast(features["label"], tf.int32)
        # 固定图片的形状，方便批处理
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        print(image_reshape, label)
        # 5.进行批处理
        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=10, num_threads=1, capacity=10)
        return image_batch, label_batch

def bin_read_manager():
    # 定义cifar的数据等命令行参数
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string("cifar_dir", "./data/bindata", "文件目录")
    tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "文件存储路径")
    # 找到文件，放入列表  路径+名字 -> 列表
    file_name = os.listdir(FLAGS.cifar_dir)
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name if file[-3:] == "bin"]
    print(file_list)

    cf = CifarRead(file_list)
    # 1.读取原二进制文件
    # img_batch, label_batch = cf.read_and_decode()

    # 3.读取tfreords文件
    image_batch, label_batch = cf.read_from_tfrecords(FLAGS.cifar_tfrecords)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启读文件线程
        threads = tf.train.start_queue_runners(sess, coord=coord)
        # 1.打印二进制读取的内容
        # print(sess.run([img_batch, label_batch]))

        # 2.存进tfrecords文件，因函数内右eval()函数，需要在session内完成
        # print("开始存储")
        # cf.write_to_tfrecords(FLAGS.cifar_tfrecords, img_batch, label_batch)
        # print("结束存储")

        # 3.打印tfrecords读取的内容
        print(sess.run([image_batch, label_batch]))

        # 回收子线程
        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    # test_queue()
    # test_muti_thread_queue()
    # csv_read_manager()
    # img_read_manager()
    bin_read_manager()

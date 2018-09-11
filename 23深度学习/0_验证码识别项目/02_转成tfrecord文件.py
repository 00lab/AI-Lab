import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("tfrecords_dir", "./tfrecords/captcha.tfrecords", "验证码tfrecords文件")
tf.app.flags.DEFINE_string("captcha_dir", "../data/Genpics/", "验证码图片路径")
tf.app.flags.DEFINE_string("letter", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "验证码字符的种类")


def dealwithlabel(label_str):

    # 构建字符索引 {0：'A', 1:'B'......}
    num_letter = dict(enumerate(list(FLAGS.letter)))

    # 键值对反转 {'A':0, 'B':1......}
    letter_num = dict(zip(num_letter.values(), num_letter.keys()))

    print(letter_num)

    # 构建标签的列表
    array = []

    # 给标签数据进行处理[[b"NZPP"]......]
    for string in label_str:

        letter_list = []# [1,2,3,4]

        # 修改编码，b'FVQJ'到字符串，并且循环找到每张验证码的字符对应的数字标记
        for letter in string.decode('utf-8'):
            letter_list.append(letter_num[letter])

        array.append(letter_list)

    # [[13, 25, 15, 15], [22, 10, 7, 10], [22, 15, 18, 9], [16, 6, 13, 10], [1, 0, 8, 17], [0, 9, 24, 14].....]
    print(array)

    # 将array转换成tensor类型
    label = tf.constant(array)

    return label


def get_captcha_image():
    """
    获取验证码图片数据
    :param file_list: 路径+文件名列表
    :return: image
    """
    # 构造文件名
    filename = []

    for i in range(6000):
        string = str(i) + ".jpg"
        filename.append(string)

    # 构造路径+文件
    file_list = [os.path.join(FLAGS.captcha_dir, file) for file in filename]

    # 构造文件队列
    file_queue = tf.train.string_input_producer(file_list, shuffle=False)

    # 构造阅读器
    reader = tf.WholeFileReader()

    # 读取图片数据内容
    key, value = reader.read(file_queue)

    # 解码图片数据
    image = tf.image.decode_jpeg(value)

    image.set_shape([20, 80, 3])

    # 批处理数据 [6000, 20, 80, 3]
    image_batch = tf.train.batch([image], batch_size=6000, num_threads=1, capacity=6000)

    return image_batch


def get_captcha_label():
    """
    读取验证码图片标签数据
    :return: label
    """
    file_queue = tf.train.string_input_producer(["../data/Genpics/labels.csv"], shuffle=False)

    reader = tf.TextLineReader()

    key, value = reader.read(file_queue)

    records = [[1], ["None"]]

    number, label = tf.decode_csv(value, record_defaults=records)

    # [["NZPP"], ["WKHK"], ["ASDY"]]
    label_batch = tf.train.batch([label], batch_size=6000, num_threads=1, capacity=6000)

    return label_batch


def write_to_tfrecords(image_batch, label_batch):
    """
    将图片内容和标签写入到tfrecords文件当中
    :param image_batch: 特征值
    :param label_batch: 标签纸
    :return: None
    """
    # 转换类型
    label_batch = tf.cast(label_batch, tf.uint8)

    print(label_batch)

    # 建立TFRecords 存储器
    writer = tf.python_io.TFRecordWriter(FLAGS.tfrecords_dir)

    # 循环将每一个图片上的数据构造example协议块，序列化后写入
    for i in range(6000):
        # 取出第i个图片数据，转换相应类型,图片的特征值要转换成字符串形式
        image_string = image_batch[i].eval().tostring()

        # 标签值，转换成整型
        label_string = label_batch[i].eval().tostring()

        # 构造协议块
        example = tf.train.Example(features=tf.train.Features(feature={
            "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
            "label": tf.train.Feature(bytes_list=tf.train.BytesList(value=[label_string]))
        }))

        writer.write(example.SerializeToString())

    # 关闭文件
    writer.close()

    return None


if __name__ == "__main__":

    # 获取验证码文件当中的图片
    image_batch = get_captcha_image()

    # 获取验证码文件当中的标签数据
    label = get_captcha_label()

    print(image_batch, label)

    with tf.Session() as sess:

        coord = tf.train.Coordinator()

        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # [b'NZPP' b'WKHK' b'WPSJ' ..., b'FVQJ' b'BQYA' b'BCHR']
        label_str = sess.run(label)

        print(label_str)

        # 处理字符串标签到数字张量
        label_batch = dealwithlabel(label_str)

        print(label_batch)

        # 将图片数据和内容写入到tfrecords文件当中
        write_to_tfrecords(image_batch, label_batch)

        coord.request_stop()

        coord.join(threads)
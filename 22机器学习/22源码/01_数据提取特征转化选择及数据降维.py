# coding=utf-8
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import jieba
import numpy as np
# import uniout  # 用于python2显示中文


def dictvec():
    """
    字典数据提取
    :return: None
    """
    # dict = DictVectorizer()
    dict = DictVectorizer(sparse=False)
    source = [{'city': "BeiJing", 'temperature':100},{'city': "ShangHai", 'temperature': 70},{'city': "ShenZhen", 'temperature': 30}]
    data = dict.fit_transform(source)
    print(dict.get_feature_names())
    print(data)
    print(dict.inverse_transform(data))
    return None


def countvec():
    """
    对文本进行特征值转换
    :return: None
    """
    cv = CountVectorizer()
    source = ["life is short, I like python","life is too long, I dislike python"]
    source = ["人生 苦短，我 用python", "人生 漫长，不用python"]  # 由此可见中文需要进行分词。使用jieba库。
    data = cv.fit_transform(source)
    print(cv.get_feature_names())
    print(data.toarray())


def cutword():
    con1 = jieba.cut("今天很残酷 明天更残酷 后天很美好 但绝对大部分是死在明天晚上 所以每个人不要放弃今天")
    con2 = jieba.cut("我们到的从很远星系来的光是在几万年之前发出的 这柞当我们肴到宇宙时,我们是在肴它的过去")
    con3 = jieba.cut("如果只用一种方式解某样車物 你就不会真正解它 了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系")
    content1 = list(con1)
    content2 = list(con2)
    content3 = list(con3)
    c1 = ' '.join(content1)
    c2 = ' '.join(content2)
    c3 = ' '.join(content3)
    return c1,c2,c3

def hanzivec():
    """
    中文特征值转化
    :return: None
    """
    cv = CountVectorizer()
    c1,c2,c3 = cutword()
    source = [c1,c2,c3]
    data = cv.fit_transform(source)
    print(cv.get_feature_names())
    print(data.toarray())


def tfidfvec():
    """
    中文特征值转化
    :return: None
    """
    c1,c2,c3 = cutword()
    print(c1,c2,c3)
    source = [c1, c2, c3]
    tf = TfidfTransformer()
    data = tf.fit_transform(source)
    print(tf.get_feature_names())
    print(data.toarray())


def mm():
    """
    归一化处理
    :return:None
    """
    mm = MinMaxScaler(feature_range=(2, 3))
    data = mm.fit_transform([[90, 2, 10, 40], [60, 4, 15, 45], [75, 3, 13, 46]])
    print(data)
    return None


def stand():
    """
    标准化缩放
    :return:None
    """
    std = StandardScaler()
    data = std.fit_transform([[3, -1, 3], [2, 4, 2], [4, 6, 1]])
    print(data)


def var():
    """
    特征选择-删除低方差的特征
    :return: None
    """
    var = VarianceThreshold(threshold=0.1)
    data = var.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
    print(data)


def im():
    """
    缺失值处理
    :return:None
    """
    # NaN, nan
    im = Imputer(missing_values='NaN', strategy='mean', axis=0)
    data = im.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
    print(data)


def pca():
    """
    主成分分析进行特征降维
    :return: None
    """
    pca = PCA(n_components=0.9)
    data = pca.fit_transform([[2, 8, 4, 5], [6, 3, 0, 8], [5, 4, 9, 1]])
    print(data)


if __name__ == '__main__':
    # dictvec()
    # countvec()
    # hanzivec()
    # tfidfvec()
    # mm()
    # stand()
    # im()
    # var()
    pca()

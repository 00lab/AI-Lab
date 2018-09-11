# coding=utf-8
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def knncls():
    """
    K-邻近预测用户签到位置
    :return: None
    """
    # 读取数据
    data = pd.read_csv("./train.csv")
    # print(data.head(10))
    # 处理数据
    # 1、缩小数据，查询数据筛选
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y > 7.5")
    # 2、处理时间
    time_value = pd.to_datetime(data["time"], unit="s")
    # print(time_value)
    # 构造特征
    time_value = pd.DatetimeIndex(time_value)
    data["day"] = time_value.day
    data["hour"] = time_value.hour
    data["weekday"] = time_value.weekday
    # 把时间戳特征删除
    data = data.drop(['time'], axis=1)
    # print(data)
    # 把签到数量少于n个目标位置删除
    place_count = data.groupby('place_id').count()
    # print(place_count)
    tf = place_count[place_count.row_id > 3].reset_index()
    # print(tf)
    data = data[data['place_id'].isin(tf.place_id)]
    data = data.drop(['row_id'], axis=1)
    # print(data)
    # 取出数据当中的特征值和目标值
    y = data['place_id']
    x = data.drop(['place_id'], axis=1)
    # 进行数据的分割训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    # 特征工程（标准化）
    std = StandardScaler()
    # 对测试集和训练集的特征值标准化
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    # 进行算法流程
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(x_train, y_train)
    # 得出预测结果
    y_predict = knn.predict(x_test)
    print("预测的目标签到位置为：", y_predict)
    print("预测的准确率：", knn.score(x_test, y_test))


def naviebayes():
    """
    朴素贝叶斯进行文本分类
    :return: None
    """
    news = fetch_20newsgroups(subset="all")
    # print(news.data)
    # print(news.target)
    # 进行数据集分割
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)
    # print(x_test)
    # 对数据集进行特征抽取
    tf = TfidfVectorizer()
    # 对训练集中的列表进行每篇文章重要性统计
    x_train = tf.fit_transform(x_train)
    print(tf.get_feature_names())
    x_test = tf.transform(x_test)
    # 进行朴素贝叶斯算法预测
    mlt = MultinomialNB(alpha=1.0)
    # print(x_train.toarray())
    mlt.fit(x_train, y_train)
    y_predict = mlt.predict(x_test)
    print("预测文章类别为：\n", y_predict)
    print("准确率为：\n", mlt.score(x_test, y_test))
    print("每个类别的精确率和召回率\n", classification_report(y_test, y_predict, target_names=news.target_names))


def gridSearchApplyToKnncls():
    """
    K-邻近预测用户签到位置
    :return: None
    """
    # 读取数据
    data = pd.read_csv("./train.csv")
    # print(data.head(10))
    # 处理数据
    # 1、缩小数据，查询数据筛选
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y > 7.5")
    # 2、处理时间
    time_value = pd.to_datetime(data["time"], unit="s")
    # print(time_value)
    # 构造特征
    time_value = pd.DatetimeIndex(time_value)
    data["day"] = time_value.day
    data["hour"] = time_value.hour
    data["weekday"] = time_value.weekday
    # 把时间戳特征删除
    data = data.drop(['time'], axis=1)
    # print(data)
    # 把签到数量少于n个目标位置删除
    place_count = data.groupby('place_id').count()
    # print(place_count)
    tf = place_count[place_count.row_id > 3].reset_index()
    # print(tf)
    data = data[data['place_id'].isin(tf.place_id)]
    data = data.drop(['row_id'], axis=1)
    # print(data)
    # 取出数据当中的特征值和目标值
    y = data['place_id']
    x = data.drop(['place_id'], axis=1)
    # 进行数据的分割训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    # 特征工程（标准化）
    std = StandardScaler()
    # 对测试集和训练集的特征值标准化
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    # 进行算法流程
    knn = KNeighborsClassifier()
    # knn.fit(x_train, y_train)
    # # 得出预测结果
    # y_predict = knn.predict(x_test)
    # print("预测的目标签到位置为：", y_predict)
    # print("预测的准确率：", knn.score(x_test, y_test))
    param = {"n_neighbors":[3, 5, 10]}
    # 构造一些参数的值进行搜索
    gc = GridSearchCV(knn, param_grid=param, cv=2)
    gc.fit(x_train, y_train)
    # 预测准确率
    print("在测试集上的准确率：\n", gc.score(x_test, y_test))
    # 在交叉验证中最好的验证结果
    print("交叉验证中最好的验证结果:\n", gc.best_score_)
    print("选择最好的模型（最游k值）是：\n", gc.best_estimator_)
    print("每个超参数每次交叉验证的结果：\n", gc.cv_results_)


def decision():
    """
    决策树 预测泰坦尼克号成员生死
    :return: None
    """
    # 获取数据
    # titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")
    titan = pd.read_csv("titanic.csv")
    #处理数据，找出特征值和目标值
    x = titan[['pclass', 'age', 'sex']]
    y = titan['survived']
    print(x)
    # 缺失值处理
    x['age'].fillna(x['age'].mean(), inplace=True)
    # 分割数据集到训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    # 进行处理（特征工程）特征-》类别-》one_hot 编码
    dict = DictVectorizer(sparse=False)
    x_train = dict.fit_transform(x_train.to_dict(orient="records"))
    print(dict.get_feature_names())
    x_test = dict.transform(x_test.to_dict(orient="records"))
    print(x_train)
    # print(x_test)
    # 用决策树进行预测
    dec = DecisionTreeClassifier()
    dec.fit(x_train, y_train)
    # 预测准确率
    print("预测的准确率：\n",dec.score(x_test, y_test))
    # 导出决策树的结构
    export_graphviz(dec, out_file="./tree.dot", feature_names=['年龄', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', '女性', '男性'])


def random_forest():
    """
    随机森林 预测泰坦尼克号成员生死
    :return: None
    """
    # 获取数据
    # titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")
    titan = pd.read_csv("titanic.csv")
    #处理数据，找出特征值和目标值
    x = titan[['pclass', 'age', 'sex']]
    y = titan['survived']
    print(x)
    # 缺失值处理
    x['age'].fillna(x['age'].mean(), inplace=True)
    # 分割数据集到训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    # 进行处理（特征工程）特征-》类别-》one_hot 编码
    dict = DictVectorizer(sparse=False)
    x_train = dict.fit_transform(x_train.to_dict(orient="records"))
    print(dict.get_feature_names())
    x_test = dict.transform(x_test.to_dict(orient="records"))
    print(x_train)
    # print(x_test)
    # 用随机森林进行预测 （超参数调优）
    rf = RandomForestClassifier()
    param = {'n_estimators':[120, 200, 300, 500, 800, 1200], 'max_depth':[5, 8, 15, 25, 30]}
    # 网格搜索与交叉验证
    gc = GridSearchCV(rf, param_grid=param, cv=2)
    gc.fit(x_train, y_train)
    print("准确率\n", gc.score(x_test, y_test))
    print("查看选择的参数模型：\n", gc.best_params_)


if __name__ == '__main__':
    # knncls()
    # naviebayes()
    # gridSearchApplyToKnncls()
    # decision()
    random_forest()

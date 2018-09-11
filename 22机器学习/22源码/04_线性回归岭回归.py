from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.externals import joblib
import pandas as pd
import numpy as np


def linear():
    """
    线性回归预测房子价格
    :return: None
    """
    # 获取数据
    lb= load_boston()
    # 分割数据到训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    # print(y_train, y_test)
    print(y_test)
    # 进行标准化处理
    # 特征值和目标值都需要进行标准化处理,实例化两个标准化API
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)

    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    # print(y_train)

    # estimator预测
    # 正规方程方式预测
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print(lr.coef_)  # 打印权重值
    # 预测测试集的房子价格
    y_lr_predict = lr.predict(x_test)
    y_lr_predict = std_y.inverse_transform(y_lr_predict)
    print("特征方程预测测试集每个房子的价格:\n",y_lr_predict)
    print("正规方程的均方误差：\n", mean_squared_error(std_y.inverse_transform(y_test), y_lr_predict))

    # 梯度下降法预测
    sgd = SGDRegressor()
    sgd.fit(x_train, y_train)
    print(sgd.coef_)  # 打印权重值
    # 预测测试集的房子价格
    y_sgd_predict = sgd.predict(x_test)
    y_predict = std_y.inverse_transform(y_sgd_predict)
    print("梯度下降法预测测试集每个房子的价格:\n", y_predict)
    print("梯度下降的均方误差：\n", mean_squared_error(std_y.inverse_transform(y_test), y_predict))

    # 回归解决过拟合：正则化。分类算法里解决过拟合的办法：1.决策树设置叶子节点的数量，2.随机森林
    # 岭回归 预测
    rd = Ridge()
    rd.fit(x_train, y_train)
    print(rd.coef_)  # 打印权重值
    # 预测测试集的房子价格
    y_rd_predict = rd.predict(x_test)
    y_predict = std_y.inverse_transform(y_rd_predict)
    print("岭回归预测测试集每个房子的价格:\n", y_predict)
    print("岭回归的均方误差：\n", mean_squared_error(std_y.inverse_transform(y_test), y_predict))
    return None


def save_model():
    """
    保存训练好的模型，用于直接使用
    :return: None
    """
    # 获取数据
    lb= load_boston()
    # 分割数据到训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    # print(y_train, y_test)
    print(y_test)
    # 进行标准化处理
    # 特征值和目标值都需要进行标准化处理,实例化两个标准化API
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)

    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    # print(y_train)

    # estimator预测
    # 正规方程方式预测
    # lr = LinearRegression()
    # lr.fit(x_train, y_train)
    # print(lr.coef_)  # 打印权重值

    # 保存训练好的模型
    # joblib.dump(lr, "test.pkl")
    # 加载保存的模型
    lr = joblib.load("test.pkl")

    # 预测测试集的房子价格
    y_lr_predict = lr.predict(x_test)
    y_lr_predict = std_y.inverse_transform(y_lr_predict)
    print("特征方程预测测试集每个房子的价格:\n",y_lr_predict)
    print("正规方程的均方误差：\n", mean_squared_error(std_y.inverse_transform(y_test), y_lr_predict))

    return None


def logistic():
    """
    逻辑回归做二分类 进行癌症预测
    :return: None
    """
    column = ['Sample code number','Clump Thickness', 'Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']
    # data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data", names=column)
    data = pd.read_csv("cancerData.csv",names=column)
    # print(data)
    # 处理缺失值
    data = data.replace(to_replace='?', value=np.nan)
    data = data.dropna()

    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)
    # 进行标准化处理
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    # 逻辑回归预测
    lg = LogisticRegression(C=1.0)
    lg.fit(x_train, y_train)
    y_predict = lg.predict(x_test)
    print(y_predict)
    print(lg.coef_)
    print("准确率:\n", lg.score(x_test, y_test))
    print("召回率：\n", classification_report(y_test, y_predict,labels=[2, 4], target_names=["良性", "恶性"]))
    return None


if __name__ == '__main__':
    # linear()
    # save_model()
    logistic()

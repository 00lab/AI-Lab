# 1.概率基础

**联合概率**：包含多个条件，且所有条件同时成立的概率

记作 𝑃(𝐴,𝐵)  、 P(AB) 、 P(A∩B)：𝑃(𝐴,𝐵) = P(A) * P(B)

**条件概率**：就是事件A在另外一个事件B已经发生条件下的发生概率

记作：𝑃(𝐴|𝐵) = P(A,B) / P(B)

**特性**：P(A1,A2|B) = P(A1|B)P(A2|B)
注意：此条件概率的成立，是由于A1,A2相互独立的结果

# 2.算法原理

朴素贝叶斯-贝叶斯公式

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815111608671-1586431802.png)

注：w为给定文档的特征值(频数统计,预测文档提供)，c为文档类别。
公式可以理解为：

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815111704799-266067737.png)

其中c可以是不同类别。

公式分为三个部分：

- - 𝑃(𝐶)：每个文档类别的概率(某文档类别词数／总文档词数)。
  - 𝑃(𝑊│𝐶)：给定类别下特征（被预测文档中出现的词）的概率。

		方法：𝑃(𝐹1│𝐶)=𝑁𝑖/𝑁	（训练文档中去计算）。

𝑁𝑖为该𝐹1词在C类别所有文档中出现的次数。

N为所属类别C下的文档所有词出现的次数和。

- - 𝑃(𝐹1,𝐹2,…) 预测文档中每个词的概率。

 

例子：

训练集统计结果(指定统计词频)：

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815112725004-428228733.png)

现有一篇被预测文档：出现了影院，支付宝，云计算，计算属于科技、娱乐的类别概率？

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815112819869-236123281.png)

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815112918495-1825386018.png)

思考：属于某个类别为0，合适吗？

# 3. 拉普拉斯平滑

问题：从上面的例子我们得到娱乐概率为0，这是不合理的，如果词频列表里面有很多出现次数都为0，很可能计算结果都为零

解决方法：**拉普拉斯平滑系数**

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815113243042-96607129.png)

𝛼为指定的系数一般为1，m为训练文档中统计出的特征词个数

# 4.sklearn朴素贝叶斯实现API

sklearn.naive_bayes.MultinomialNB

sklearn.naive_bayes.MultinomialNB(alpha = 1.0)朴素贝叶斯分类

alpha：拉普拉斯平滑系数

# 5. 分类模型的评估

**(1) 准确率**

estimator.score()
一般最常见使用的是准确率，即预测结果正确的百分比。

**(2) 精确率和召回率**

- - **混淆矩阵**

在分类任务下，预测结果(Predicted Condition)与正确标记(True Condition)之间存在四种不同的组合，构成混淆矩阵(适用于多分类)

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815185010155-992942323.png)

 

- - **精确率**

预测结果为正例样本中真实为正例的比例（查得准）

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815184614672-1647029296.png)

 

- - **召回率**

真实为正例的样本中预测结果为正例的比例（查的全，对正样本的区分能力）

 ![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815184624382-1838134210.png)

- - **其他分类标准**，F1-score，反映了模型的稳健型

![img](https://images2018.cnblogs.com/blog/964076/201808/964076-20180815184757864-1389733235.png)

 

**(3) 分类模型评估API**

sklearn.metrics.classification_report

sklearn.metrics.classification_report(y_true, y_pred, target_names=None)

- - y_true：真实目标值
  - y_pred：估计器预测目标值
  - target_names：目标类别名称
  - return：每个类别精确率与召回率

# 6. 朴素贝叶斯算法案例

sklearn20类新闻分类
20个新闻组数据集包含20个主题的18000个新闻组帖子

``` python
# coding=utf-8
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd


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


if __name__ == '__main__':
    naviebayes()
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

#  7. 朴素贝叶斯分类优缺点

优点：

- 朴素贝叶斯模型发源于古典数学理论，有稳定的分类效率。
- 对缺失数据不太敏感，算法也比较简单，常用于文本分类。
- 分类准确度高，速度快

缺点：

- 需要知道先验概率P(F1,F2,…|C)，因此在某些时候会由于假设的先验
- 模型的原因导致预测效果不佳。
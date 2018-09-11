# AI-Lab - 验证码识别项目

<font color="#0000dd">验证码识别项目主要包含 生成验证码数据集、将数据集保存成tfrecord格式、训练预测模型三大块</font>

# 1.生成验证码数据集

> 参考文章
> 1. https://cloud.tencent.com/developer/article/1052886
> 2. https://www.cnblogs.com/6324TV/p/8811249.html

## 1.1 从网络下载验证码

根据文章1提供的便利，从http://cuijiahua.com/tutrial/discuz/index.php?label= 中下载验证码文件，不过下载到1732张后就报错了，Url Error: Connection refused。
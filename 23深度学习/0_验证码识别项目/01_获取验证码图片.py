# coding:utf-8
from urllib.request import urlretrieve
import time, random, os


class CaptchaFactory():
    # 代码参考博客： https://cloud.tencent.com/developer/article/1052886
    def __init__(self):
        # 验证码生成图片地址
        self.url = 'http://cuijiahua.com/tutrial/discuz/index.php?label='

    def __random_captcha_text(self, captcha_size=4):
        """
        验证码一般都无视大小写；验证码长度4个字符
        Parameters:
          captcha_size:验证码长度
        Returns:
          captcha_text:验证码字符串
        """
        # number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        # char_set = number + alphabet
        # 第一阶段只产生纯字母的验证码
        char_set = alphabet
        captcha_text = []
        for i in range(captcha_size):
            c = random.choice(char_set)
            captcha_text.append(c)
        captcha_text = ''.join(captcha_text)
        return captcha_text

    def download_captcha_img(self, dir_name='./CaptchaData', nums=100):
        """
        下载验证码图片
        Parameters:
          dirname = 验证码图片存放的路径
          nums:下载的验证码图片数量
        """
        if dir_name[2:] not in os.listdir():
            os.mkdir(dir_name)
        for i in range(nums):
            label = self.__random_captcha_text()
            print('第%d张图片:%s下载' % (i + 1, label))
            urlretrieve(url=self.url + label, filename=dir_name + '/' + label + '.jpg')
            # 博主交代:请至少加200ms延时，避免给服务器造成过多的压力，如发现影响服务器正常工作，会关闭此功能。
            time.sleep(0.2)
        print('图片下载完成！')

    def download_captcha_img_map_file(self, dir_name='./CaptchaData', nums=3000):
        """
        下载验证码图片到文件夹，并将图片验证码的内容保存在一一对应的csv文件上
        Parameters:
          dirname = 验证码图片存放的路径
          nums:下载的验证码图片数量
        """
        # print(os.listdir())
        if dir_name[2:] not in os.listdir(path="./"):
            os.mkdir(dir_name)
        csv = open(dir_name+"/captchaText.csv", "a+")
        for i in range(1732,nums):
            label = self.__random_captcha_text()
            print('第%d张图片:%s下载' % (i + 1, label))
            csv.writelines(label+"\n")
            # 默认下载的图片是100×30
            urlretrieve(url=self.url + label + '&width=80&height=20', filename=dir_name + '/' + str(i) + '.jpg')
            # 博主交代:请至少加200ms延时，避免给服务器造成过多的压力，如发现影响服务器正常工作，会关闭此功能。
            time.sleep(0.2)
        csv.close()
        print('图片下载完成！')


if __name__ == '__main__':
    cf = CaptchaFactory()
    cf.download_captcha_img_map_file()
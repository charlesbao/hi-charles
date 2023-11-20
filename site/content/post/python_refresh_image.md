+++
date = "2023-12-10T17:02:45+08:00"
tags = ["Python","脚本","方法"]
title = "Python 远程桌面图像对比刷新方法"

+++

> Python远程桌面中图像对比刷新以提高效率<!--more-->

使用Pil截取屏幕，并切分图像，对比差异，只刷新不相同区块，用于远程桌面的情况下，将大大减少带宽使用率。

```
from PIL import ImageGrab, Image  
from base64 import encodestring  
import time

def takePhoto(cropK,photoSize,im_old):  
    # 截取屏幕
    im = ImageGrab.grab()
    if photoSize != 0:
        ## 压缩图像 降低CPU压力
        im.thumbnail((photoSize,photoSize))
    width,height = im.size
    eachWidth = width/cropK
    eachHeight = height/cropK
    arr = []
    for each1 in range(0,cropK):
        ##
        for each2 in range(0,cropK):
            ### 依次裁切图像，并与之前图像做对比，如果不相同则输出
            box = (eachWidth * each1,eachHeight * each2,eachWidth * (each1 + 1),eachHeight * (each2 + 1))
            region = im.crop(box)
            if not region.tostring() == im_old[each1][each2]:
                region.save('tmp.jpg','jpeg')
                arr.append([each1,each2,encodestring(open('tmp.jpg','rb').read())])
                im_old[each1][each2] = region.tostring()
            ####
    if len(arr) != 0:
        ## 得到base64编码格式的分割图片list，里面包含 【x轴位置信息，y轴位置信息，base64图像信息】
        print arr

def init(data):  
    # 初始化
    im_old = []
    for each1 in range(0,data['cropK']):
        ##
        imTmp = []
        for each2 in range(0,data['cropK']):
            imTmp.append(None)
        im_old.append(imTmp)
    #
    while True:
        ## 循环截屏
        takePhoto(data['cropK'],data['photoSize'],im_old)
        time.sleep(data['sleepTime'])
    #

if __name__ == '__main__':  
    #
    data = {
        ## 截屏切割段数 此为 5的平方
        cropK: 5,
        ## 截屏压缩比率，0 为不压缩，此外数值越高图像质量越好
        photoSize: 0,
        ## 截屏刷新频率
        sleepTime: 0.2
    }
    init(data)
```
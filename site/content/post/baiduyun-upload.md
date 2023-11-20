+++
date = "2022-06-04T00:00:00Z"
tags = ["Python","方法"]
title = "百度网盘存储资源解决方案"
+++

> 使用百度网盘作为存储媒介的Python脚本<!--more-->

**安装两个依赖库**
```
#进度条第三方库
pip install progressbar
#百度云盘第三方库
pip install baidupcsapi
```

**运行上传脚本**  
运行时需要进行验证码验证，请先在有浏览器的电脑上登陆一次，再将其生成的cookies传到要上传文件的服务器中即可自动登陆。  
脚本遍历上传"./upload"目录下的所有文件，大文件将自动切片上传。 
 
**参数**  
`username` 　百度云用户名  
`password` 　百度云密码  
`remotePath` 　存放百度云文件夹 更目录为"/"  

`python bd_uploadFromDir.py` 　运行脚本 
```
#coding: utf-8
import os,json,sys,tempfile
from baidupcsapi import PCS
import progressbar

class ProgressBar():
    def __init__(self):
        self.first_call = True
    def __call__(self, *args, **kwargs):
        if self.first_call:
            self.widgets = [progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker('>')),
                            ' ', progressbar.FileTransferSpeed()]
            self.pbar = progressbar.ProgressBar(widgets=self.widgets, maxval=kwargs['size']).start()
            self.first_call = False

        if kwargs['size'] <= kwargs['progress']:
            self.pbar.finish()
        else:
            self.pbar.update(kwargs['progress'])


def upload(filePath,remotePath):
    fid = 1
    md5list = []

    with open(filePath, 'rb') as infile:
        while 1:
            data = infile.read(chunkSize)
            if len(data) == 0: break
            smallfile = os.path.join(tmpDir, 'tmp%d' % fid)
            with open(smallfile, 'wb') as f:
                f.write(data)
            print('chunk%d size %d' % (fid, len(data)))
            fid += 1
            print('start uploading...')
            ret = pcs.upload_tmpfile(open(smallfile, 'rb'), callback=ProgressBar())
            md5list.append(json.loads(ret.content)['md5'])
            print('md5: %s' % (md5list[-1]))
            os.remove(smallfile)
    pcs.upload_superfile(os.path.join(remotePath,os.path.basename(filePath)), md5list)

pcs = PCS(username,password)
chunkSize = 1024*1024*64
tmpDir = tempfile.mkdtemp('bdpcs')
remotePath = remotePath

for each in os.listdir('upload'):
    print 'upload',each
    upload(os.path.join('upload',each),remotePath)
    print 'finish',each

os.rmdir(tmpDir)
```

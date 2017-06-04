+++
date = "2017-06-01T00:00:00Z"
tags = ["Python","方法"]
title = "Python 阿里云oss存储 小文件上传下载"

+++

> 阿里云oss对象存储，使用官方api上传下载文件<!--more-->

# Python 阿里云oss存储 小文件上传下载

**阿里云 Python sdk的实践**  
根据参数配置上传路径、下载路径等

`python uploadToOSS.py` 　运行脚本
```
# -*- coding: utf-8 -*-

import oss2
import os
from optparse import OptionParser

def getService():
    service = oss2.Service(AUTH, END_POINT)
    print([b.name for b in oss2.BucketIterator(service)])

def uploadBucket(localFile,remoteFolder = ""):
    bucket = oss2.Bucket(AUTH, END_POINT, bucket_name=BUCKET_NAME)
    (_,remoteFileName) = os.path.split(localFile)
    remoteFile = os.path.join(remoteFolder,remoteFileName)
    print "start upload",remoteFileName
    bucket.put_object_from_file(remoteFile, localFile)
    print "finish upload",remoteFileName

def downloadBucket(remoteFileName,remoteFolder = ""):
    bucket = oss2.Bucket(AUTH, END_POINT, bucket_name=BUCKET_NAME)
    localFile = os.path.join("download",remoteFileName)
    remoteFile = os.path.join(remoteFolder,remoteFileName)
    print "start download",remoteFileName
    bucket.get_object_to_file(remoteFile, localFile)
    print "finish download",remoteFileName

END_POINT = endPoint  
AUTH = Auth(apiKey, apiSecrets)
BUCKET_NAME = bucketName

parser = OptionParser()
parser.add_option("-f", "--files", dest="filenames",
                  help="action for filenames,split by ',',like [1.txt,2.txt]")
parser.add_option("-t", "--type",
                  dest="type", default="download",
                  help="type name [download] or [upload],[default: %default]")
parser.add_option("-d", "--dest",
                  dest="dest", default="",
                  help="remoteFolder for download or upload")
(options, args) = parser.parse_args()
if options.type == "download":
    for remoteFileName in options.filenames.split(','):
        print remoteFileName
        downloadBucket(remoteFileName,options.dest)
elif options.type == "upload":
    for localFileName in options.filenames.split(','):
        uploadBucket(localFileName,options.dest)
else:
    os._exit(1)



```


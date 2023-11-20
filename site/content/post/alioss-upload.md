+++
date = "2022-06-05T00:00:00Z"
tags = ["Python","方法"]
title = "Python 阿里云OSS存储断点续传"

+++

> 阿里云oss对象存储，使用断点续传来上传大文件<!--more-->

**安装阿里云oss2库**
```
pip install oss2
```
**根据命令上传文件到oss**
  
`apiKey` 　accessKey中的键  
`apiSecrets` 　accessKey中的密钥  
`endPoint` 　oss服务公网地址    
`bucketName` 　存储的bucket名字    
参数：  
`-f <要上传的文件路径>` 　上传文件路径    
`-d <远程文件存放路径>` 　远程文件路径  

`python upload.py` 　运行脚本
```
import os
from oss2 import SizedFileAdapter, determine_part_size, Bucket, Auth
from oss2.models import PartInfo
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-f", "--files", dest="filenames",
                  help="action for filenames,split by ',',like [1.txt,2.txt]")
parser.add_option("-d", "--dest",
                  dest="dest", default="",
                  help="remoteFolder for download or upload")
(options, args) = parser.parse_args()

key = options.dest
filename = options.filenames
total_size = os.path.getsize(filename)
part_size = determine_part_size(total_size, preferred_size=100 * 1024)

END_POINT = endPoint
AUTH = Auth(apiKey, apiSecrets)
BUCKET_NAME = bucketName
bucket = Bucket(AUTH, END_POINT, bucket_name=BUCKET_NAME)
upload_id = bucket.init_multipart_upload(key).upload_id
parts = []
with open(filename, 'rb') as fileobj:
    part_number = 1
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        result = bucket.upload_part(key, upload_id, part_number,
                                    SizedFileAdapter(fileobj, num_to_upload))
        parts.append(PartInfo(part_number, result.etag))
        offset += num_to_upload
        part_number += 1

bucket.complete_multipart_upload(key, upload_id, parts)
```
**上传./upload文件夹的所有资源**  

`apiKey` 　accessKey中的键  
`apiSecrets` 　accessKey中的密钥  
`endPoint` 　oss服务公网地址    
`remotePath` 　远程存放文件的路径    
`bucketName` 　存储的bucket名字    

`python ./uploadFromDir.py` 　运行脚本  
```
import os
from oss2 import SizedFileAdapter, determine_part_size, Bucket, Auth
from oss2.models import PartInfo

def upload(filename,key):
    total_size = os.path.getsize(filename)
    part_size = determine_part_size(total_size, preferred_size=100 * 1024)

    END_POINT = endPoint
    AUTH = Auth(apiKey, apiSecrets)
    BUCKET_NAME = bucketName
    bucket = Bucket(AUTH, END_POINT, bucket_name=BUCKET_NAME)

    upload_id = bucket.init_multipart_upload(key).upload_id
    parts = []
    with open(filename, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(key, upload_id, part_number,
                                        SizedFileAdapter(fileobj, num_to_upload))
            parts.append(PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1

    bucket.complete_multipart_upload(key, upload_id, parts)

for each in os.listdir('upload'):
    print 'upload',each
    upload(os.path.join('upload',each),os.path.join(remotePath,each))
    print 'finish',each
```
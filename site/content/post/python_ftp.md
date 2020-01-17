+++
date = "2018-05-06T00:00:00Z"
tags = ["Python","方法"]
title = "使用Python创建ftp服务器"

+++

> Python的pyftpdlib可用于创建ftp服务器<!--more-->

使用Python能够轻易创建一个ftp服务器，并可以使用Pyinstaller打包成可执行程序，在无Python环境的电脑中使用
```
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

import os

def getDisk():
    arr = []
    for i in range(65,91):
        vol=chr(i)+':'
        if os.path.isdir(vol):
            arr.append(vol)
    return arr


def main(disks):
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', '/')
    for i in disks:
        authorizer.add_user(i+'user', '12345', i+'\\')
    handler = FTPHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer(('0.0.0.0', 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    main(getDisk())
```
----
**解释**
```
def getDisk()
```
* 其作用为遍历Windows所有磁盘，并返回可用磁盘
```
authorizer.add_user(i+'user', '12345', i+'\\')
```
* i为盘符名 如 C:,D:;
* 其作用为创建以盘符为首的用户名，密码为12345，默认路径为盘符根目录
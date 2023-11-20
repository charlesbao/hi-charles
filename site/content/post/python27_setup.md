+++
date = "2022-05-25T00:00:00Z"
tags = ["Python","centos","方法"]
title = "centos 安装Python2.7"

+++

> centos默认安装的是Python2.6版本，有些模块使用会出错，这里是我安装Python2.7.9的全部过程<!--more-->

首先需要安装Development tools
```
yum groupinstall "Development tools"
```
安装编译Python需要的依赖包
```
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel -y
```
下载并解压Python 2.7.9的源代码
```
cd /opt
wget --no-check-certificate https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
tar xf Python-2.7.9.tar.xz
cd Python-2.7.9
```
编译与安装Python 2.7.9
```
./configure --prefix=/usr/local
make && make altinstall
```
将python命令指向Python 2.7.9
```
ln -s /usr/local/bin/python2.7 /usr/local/bin/python
```
检查Python版本
```
python -v
```
安装PIP
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
> 至此，Python2.7与pip都安装完成。
+++
date = "2022-06-05T00:00:00Z"
tags = ["filesystem","linux","方法"]
title = "Linux使用NFS挂载远程硬盘"

+++
> NFS即网络文件系统，可以将多台Linux服务器之间进行硬盘数据共享，使用挂载的方式共享文件<!--more-->

## 定义
服务端IP: `192.168.1.2`  
客户端IP: `192.168.1.1`    

## 配置服务端

安装nfs-server
```
#centos
yum install -y nfs-utils rpcbind 
#ubuntu/debian
apt-get install nfs-common nfs-kernel-server
```

**[可选]**搜索和设置如下所示的端口配置：  
vi /etc/sysconfig/nfs
```RQUOTAD_PORT=30001
LOCKD_TCPPORT=30002
LOCKD_UDPPORT=30002
MOUNTD_PORT=30003
STATD_PORT=30004
```
**[可选]**创建共享目录
```
mkdir /home/nfs_share
```
配置exports文件 `vi /etc/exports `   
```
/home/nfs_share 192.168.1.1(rw,sync,no_root_squash)
共享路径 客户端IP[可选 * ]
```

开机自动启动，重启服务  
```
#centos
chkconfig nfs on
chkconfig rpcbind on
service nfs restart
service rpcbind restart

#ubuntu
chkconfig nfs-kernel-server on
service nfs-kernel-server restart
```
---

## 配置客户端  

安装nfs-client  
```
#centos
yum install -y nfs-utils
#ubuntu/debian
apt-get install nfs-common
```

查看挂载点
```
showmount -e 192.168.1.2
```
**[可选]**创建挂载目录
```
mkdir -p /root/mnt_dir
```
挂载共享目录
```
mount -t nfs 192.168.1.2:/data/nfs_share /root/mnt_dir
```
开机自动挂载 `vi /etc/fstab`
```
192.168.1.2:/data/nfs_share /root/mnt_dir nfs defaults 0 0
```

---
**[可选]**卸载共享目录
```
umount -l /root/remote_dir
```
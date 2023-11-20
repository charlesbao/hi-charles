+++
date = "2022-05-26T00:00:00Z"
tags = ["vpn","centos","脚本"]
title = "centos6下一键配置http代理"

+++

> 一键安装squid代理服务器的shell脚本<!--more-->

此安装脚本可运行在Centos x86/x64 下的最小系统版本中。 
可运行于openvz，kvm，xen虚拟环境中。  
将在相应目录创建一个`proxy-secrets`的用户认证文件软链接方便管理用户
```
#! /bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin  
export PATH
SECRETS_PATH=/root/secrets
if [[ $EUID -ne 0 ]]; then  
   echo "Error:This script must be run as root!" 1>&2
   exit 1
fi  
mkdir -p ${SECRETS_PATH}
setenforce 0
ulimit -n 800000
echo "* soft nofile 800000" >> /etc/security/limits.conf
echo "* hard nofile 800000" >> /etc/security/limits.conf
echo "alias net-pf-10 off" >> /etc/modprobe.d/dist.conf
echo "alias ipv6 off" >> /etc/modprobe.d/dist.conf
killall sendmail
/etc/init.d/postfix stop
chkconfig --level 2345 postfix off
chkconfig --level 2345 sendmail off
yum -y install squid
cat > /etc/squid/squid.conf <<-EOF
auth_param basic program /usr/bin/python /etc/squid/auth.py
auth_param basic children 5
auth_param basic realm Welcome to wofanvpn.cn proxy web server
acl manager proto cache_object

acl localhost dst 127.0.0.0/8 0.0.0.0/32 ::1
acl SSL_ports port 443
acl Safe_ports port 80          # http
acl Safe_ports port 21          # ftp
acl Safe_ports port 443         # https
acl Safe_ports port 70          # gopher
acl Safe_ports port 210         # wais
acl Safe_ports port 1025-65535  # unregistered ports
acl Safe_ports port 280         # http-mgmt
acl Safe_ports port 488         # gss-http
acl Safe_ports port 591         # filemaker
acl Safe_ports port 777         # multiling http
acl CONNECT method CONNECT
acl squid_user proxy_auth REQUIRED
http_access allow squid_user
http_access allow manager localhost
http_access deny manager
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access deny all

http_port 25
coredump_dir /var/spool/squid
refresh_pattern -i ^ftp:            525600    95% 525600 reload-into-ims
refresh_pattern -i (/cgi-bin/|\?)   0          0% 0      reload-into-ims
refresh_pattern -i .                525600    95% 525600 reload-into-ims
strip_query_terms off
visible_hostname wofanvpn.cn
cache_mgr hi@charlesbao.com
cache_store_log none
cache_access_log none
cache_mem 512 MB
cache_dir aufs /var/cache/squid 5000 128 128
cache_swap_low 90
cache_swap_high 95
maximum_object_size 128 MB
maximum_object_size_in_memory 128 MB
dns_nameservers 8.8.8.8 8.8.4.4
client_lifetime 1 minutes
half_closed_clients off
fqdncache_size 65535
ipcache_size 65535
ipcache_low 90
ipcache_high 95
EOF
cat > /etc/squid/proxy-secrets <<-EOF
iwofan 123123 #
EOF
cat > /etc/squid/auth.py <<-EOF
#!/usr/bin/python
#coding:utf-8
import sys

fp = open('/etc/squid/proxy-secrets','r')
contents = fp.read()
fp.close()

line = sys.stdin.readline()
fields = line.replace('\n',' #')
if fields in contents:
    sys.stdout.write('OK\n')
else:
    sys.stdout.write('ERR\n')
EOF
mkdir -p /var/cache/squid
chmod -R 777 /var/cache/squid
squid -z
service squid restart
chkconfig --level 2345 squid on
iptables -t nat -F
iptables -t nat -X
iptables -t nat -P PREROUTING ACCEPT
iptables -t nat -P POSTROUTING ACCEPT
iptables -t nat -P OUTPUT ACCEPT
iptables -t mangle -F
iptables -t mangle -X
iptables -t mangle -P PREROUTING ACCEPT
iptables -t mangle -P INPUT ACCEPT
iptables -t mangle -P FORWARD ACCEPT
iptables -t mangle -P OUTPUT ACCEPT
iptables -t mangle -P POSTROUTING ACCEPT
iptables -F
iptables -X
iptables -P FORWARD ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -t raw -F
iptables -t raw -X
iptables -t raw -P PREROUTING ACCEPT
iptables -t raw -P OUTPUT ACCEPT
service iptables save
service iptables restart
ln -s /etc/squid/proxy-secrets ${SECRETS_PATH}/proxy-secrets
```
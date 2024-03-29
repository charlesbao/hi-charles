+++
date = "2022-05-25T00:00:00Z"
tags = ["vpn","linux","脚本"]
title = "搭建shadowsocks 超越翻墙的翻墙方式"
draft = true
+++

> Shadowsocks比PPTP翻墙更加方便稳定，且不会被某些运营商屏蔽，方便又快捷（此篇为搭建翻墙服务器所用）<!--more-->

以下是linux服务器对shadowsocks的配置shell源码，方便阅读。

或将以下源码复制黏贴于.sh的文件中 777权限 ./运行即可哦

```
#! /bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
#===============================================================================================
#   System Required:  CentOS 6,7, Debian, Ubuntu
#   Description:  One click Install Shadowsocks(Python)
#===============================================================================================

clear
echo ""
echo "#############################################################"
echo "# One click Install Shadowsocks(Python)"
echo "# System Required:  CentOS 6,7, Debian, Ubuntu"
echo "#############################################################"
echo ""

# Make sure only root can run our script
function rootness(){
    if [[ $EUID -ne 0 ]]; then
       echo "Error:This script must be run as root!" 1>&2
       exit 1
    fi
}

# Check OS
function checkos(){
    if [ -f /etc/redhat-release ];then
        OS=CentOS
    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        OS=Debian
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        OS=Ubuntu
    else
        echo "Not support OS, Please reinstall OS and retry!"
        exit 1
    fi
}

# Get version
function getversion(){
    if [[ -s /etc/redhat-release ]];then
        grep -oE  "[0-9.]+" /etc/redhat-release
    else    
        grep -oE  "[0-9.]+" /etc/issue
    fi    
}

# CentOS version
function centosversion(){
    local code=$1
    local version="`getversion`"
    local main_ver=${version%%.*}
    if [ $main_ver == $code ];then
        return 0
    else
        return 1
    fi        
}

# Disable selinux
function disable_selinux(){
if [ -s /etc/selinux/config ] && grep 'SELINUX=enforcing' /etc/selinux/config; then
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
    setenforce 0
fi
}

# Pre-installation settings
function pre_install(){
    # Not support CentOS 5
    if centosversion 5; then
        echo "Not support CentOS 5.x, please change to CentOS 6,7 or Debian or Ubuntu and try again."
        exit 1
    fi
    #Set shadowsocks config password
    echo "Please input password for shadowsocks:"
    read -p "(Default password: howhost.me):" shadowsockspwd
    if [ "$shadowsockspwd" = "" ]; then
        shadowsockspwd="howhost.me"
    fi
    IP=$(curl -s -4 ipinfo.io | grep "ip" | awk -F\" '{print $4}')
    echo "Please input IP for shadowsocks:"
    read -p "(Default IP: ${IP}):" shadowsocksip
    if [ "$shadowsockspwd" = "" ]; then
        shadowsocksip="${IP}"
    fi
    echo "password:$shadowsockspwd"
    echo "####################################"
    get_char(){
        SAVEDSTTY=`stty -g`
        stty -echo
        stty cbreak
        dd if=/dev/tty bs=1 count=1 2> /dev/null
        stty -raw
        stty echo
        stty $SAVEDSTTY
    }
    echo ""
    echo "Press any key to start...or Press Ctrl+C to cancel"
    char=`get_char`
    #Install necessary dependencies
    if [ "$OS" == 'CentOS' ]; then
        yum install -y wget unzip openssl-devel gcc swig python python-devel python-setuptools autoconf libtool libevent
        yum install -y automake make curl curl-devel zlib-devel perl perl-devel cpio expat-devel gettext-devel
    else
        apt-get -y update
        apt-get -y install python python-dev python-pip curl wget unzip gcc swig automake make perl cpio
    fi
    # Get IP address
    echo "Getting Public IP address, Please wait a moment..."
    echo -e "Your main public IP is\t\033[32m$IP\033[0m"
    echo ""
    #Current folder
    cur_dir=`pwd`
    cd $cur_dir
}

# Download files
function download_files(){
    if [ "$OS" == 'CentOS' ]; then
        if ! wget --no-check-certificate -O ez_setup.py https://bootstrap.pypa.io/ez_setup.py; then
            echo "Failed to download ez_setup.py!"
            exit 1
        fi
        # Download shadowsocks chkconfig file
        if ! wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks -O /etc/init.d/shadowsocks; then
            echo "Failed to download shadowsocks chkconfig file!"
            exit 1
        fi
    else
        if ! wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-debian -O /etc/init.d/shadowsocks; then
            echo "Failed to download shadowsocks chkconfig file!"
            exit 1
        fi
    fi
}

# Config shadowsocks
function config_shadowsocks(){
    cat > /etc/shadowsocks.json<<-EOF
{
    "server":"${IP}",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "port_password":{
    "8989":"${shadowsockspwd}"
    },
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
}
EOF
}

# iptables set
function iptables_set(){
    echo "iptables start setting..."
    /sbin/service iptables status 1>/dev/null 2>&1
    if [ $? -eq 0 ]; then
        /etc/init.d/iptables status | grep '8989' | grep 'ACCEPT' >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            /sbin/iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 8989 -j ACCEPT
            /etc/init.d/iptables save
            /etc/init.d/iptables restart
        else
            echo "port 8989 has been set up."
        fi
    else
        echo "iptables looks like shutdown, please manually set it if necessary."
    fi
}

# Install Shadowsocks
function install_ss(){
    which pip > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        if [ "$OS" == 'CentOS' ]; then
            python ez_setup.py install
            easy_install pip
        fi
    fi
    if [ -f /usr/bin/pip ]; then
        pip install M2Crypto
        pip install greenlet
        pip install gevent
        pip install shadowsocks
        if [ -f /usr/bin/ssserver ] || [ -f /usr/local/bin/ssserver ]; then
            chmod +x /etc/init.d/shadowsocks
            # Add run on system start up
            if [ "$OS" == 'CentOS' ]; then
                chkconfig --add shadowsocks
                chkconfig shadowsocks on
            else
                update-rc.d shadowsocks defaults
            fi
            # Run shadowsocks in the background
            /etc/init.d/shadowsocks start
        else
            echo ""
            echo "Shadowsocks install failed!"
            exit 1
        fi
        clear
        echo ""
        echo "Congratulations, shadowsocks install completed!"
        cat /etc/shadowsocks.json
        exit 0
    else
        echo ""
        echo "pip install failed!"
        exit 1
    fi
}

# Uninstall Shadowsocks
function uninstall_shadowsocks(){
    printf "Are you sure uninstall Shadowsocks? (y/n) "
    printf "\n"
    read -p "(Default: n):" answer
    if [ -z $answer ]; then
        answer="n"
    fi
    if [ "$answer" = "y" ]; then
        ps -ef | grep -v grep | grep -v ps | grep -i "ssserver" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            /etc/init.d/shadowsocks stop
        fi
        checkos
        if [ "$OS" == 'CentOS' ]; then
            chkconfig --del shadowsocks
        else
            update-rc.d -f shadowsocks remove
        fi
        # delete config file
        rm -f /etc/shadowsocks.json
        rm -f /var/run/shadowsocks.pid
        rm -f /etc/init.d/shadowsocks
        pip uninstall -y shadowsocks
        if [ $? -eq 0 ]; then
            echo "Shadowsocks uninstall success!"
        else
            echo "Shadowsocks uninstall failed!"
        fi
    else
        echo "uninstall cancelled, Nothing to do"
    fi
}

# Install Shadowsocks-python
function install_shadowsocks(){
    checkos
    rootness
    disable_selinux
    pre_install
    download_files
    config_shadowsocks
    if [ "$OS" == 'CentOS' ]; then
        if ! centosversion 7; then
            iptables_set
        fi
    fi
    install_ss
}

# Initialization step
action=$1
[  -z $1 ] && action=install
case "$action" in
install)
    install_shadowsocks
    ;;
uninstall)
    uninstall_shadowsocks
    ;;
*)
    echo "Arguments error! [${action} ]"
    echo "Usage: `basename $0` {install|uninstall}"
    ;;
esac
```
* 如果没有报错的话，shadowsocks的安装配置就完成啦。
* 端口和密码的配置文件在/etc/shadowsocks.json文件中。


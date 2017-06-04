+++
date = "2017-05-26T00:00:00Z"
tags = ["ngrok","linux","vpn","脚本"]
title = "Ngrok 内网穿透安装脚本"

+++

> ngrok 是一个反向代理，通过在公共的端点和本地运行的 Web 服务器之间建立一个安全的通道.<!--more-->

**为方便安装server及生成client，开发以下脚本**  

Ngrok server&client 安装工具
```
#!/bin/bash
# -*- coding: UTF-8 -*-

SELFPATH=$(cd "$(dirname "$0")"; pwd)

echo 'input a domain'
read DOMAIN
install_depends(){
	yum -y install zlib-devel openssl-devel perl hg cpio expat-devel gettext-devel curl curl-devel perl-ExtUtils-MakeMaker hg wget gcc gcc-c++ build-essential mercurial zip
}

install_git(){
	unstall_git
	if [ ! -f $SELFPATH/git-2.6.0.tar.gz ];then
		wget https://www.kernel.org/pub/software/scm/git/git-2.6.0.tar.gz
	fi
	tar zxvf git-2.6.0.tar.gz
	cd git-2.6.0
	./configure --prefix=/usr/local/git
	make
	make install
	ln -s /usr/local/git/bin/* /usr/bin/
	rm -rf $SELFPATH/git-2.6.0
}

unstall_git(){
	rm -rf /usr/local/git
	rm -rf /usr/local/git/bin/git
	rm -rf /usr/local/git/bin/git-cvsserver
	rm -rf /usr/local/git/bin/gitk
	rm -rf /usr/local/git/bin/git-receive-pack
	rm -rf /usr/local/git/bin/git-shell
	rm -rf /usr/local/git/bin/git-upload-archive
	rm -rf /usr/local/git/bin/git-upload-pack
}


install_go(){
	cd $SELFPATH
	uninstall_go
	ldconfig
	if [ $(getconf WORD_BIT) = '32' ] && [ $(getconf LONG_BIT) = '64' ];then
		if [ ! -f $SELFPATH/go1.4.2.linux-amd64.tar.gz ];then
			wget http://www.golangtc.com/static/go/1.4.2/go1.4.2.linux-amd64.tar.gz
		fi
	    tar zxvf go1.4.2.linux-amd64.tar.gz
	else
		if [ ! -f $SELFPATH/go1.4.2.linux-386.tar.gz ];then
			wget http://www.golangtc.com/static/go/1.4.2/go1.4.2.linux-386.tar.gz
		fi
	    tar zxvf go1.4.2.linux-386.tar.gz
	fi
	mv go /usr/local/
	ln -s /usr/local/go/bin/* /usr/bin/
}

uninstall_go(){
	rm -rf /usr/local/go
	rm -rf /usr/bin/go
	rm -rf /usr/bin/godoc
	rm -rf /usr/bin/gofmt
}

install_ngrok(){
	uninstall_ngrok
	cd /usr/local
	if [ ! -f /usr/local/ngrok ];then
		cd /usr/local/
		git clone https://github.com/inconshreveable/ngrok.git ngrok
	fi
	export GOPATH=/usr/local/ngrok/
	export NGROK_DOMAIN=$DOMAIN
	cd ngrok
	openssl genrsa -out rootCA.key 2048
	openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=$NGROK_DOMAIN" -days 5000 -out rootCA.pem
	openssl genrsa -out server.key 2048
	openssl req -new -key server.key -subj "/CN=$NGROK_DOMAIN" -out server.csr
	openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 5000
	cp rootCA.pem assets/client/tls/ngrokroot.crt
	cp server.crt assets/server/tls/snakeoil.crt
	cp server.key assets/server/tls/snakeoil.key
	sed -i 's#code.google.com/p/log4go#github.com/keepeye/log4go#' /usr/local/ngrok/src/ngrok/log/logger.go
	
	GOOS=`go env | grep GOOS | awk -F\" '{print $2}'`
	GOARCH=`go env | grep GOARCH | awk -F\" '{print $2}'`
	cd /usr/local/go/src
	GOOS=$GOOS GOARCH=$GOARCH ./make.bash
	cd /usr/local/ngrok
	GOOS=$GOOS GOARCH=$GOARCH make release-server
}

# 卸载ngrok
uninstall_ngrok(){
	rm -rf /usr/local/ngrok
}

# 编译客户端
compile_client(){
	cd /usr/local/go/src
	GOOS=$1 GOARCH=$2 ./make.bash
	cd /usr/local/ngrok/
	GOOS=$1 GOARCH=$2 make release-client
	zip -r /root/$1_$2.zip /usr/local/ngrok/bin/$1_$2
}

# 生成客户端
client(){
	echo "1.Linux 32"
	echo "2.Linux 64"
	echo "3.Windows 32"
	echo "4.Windows 64"
	echo "5.Mac OS 32"
	echo "6.Mac OS 64"
	echo "7.Linux ARM"

	read num
	case "$num" in
		[1] )
			compile_client linux 386
		;;
		[2] )
			compile_client linux amd64
		;;
		[3] )
			compile_client windows 386
		;;
		[4] ) 
			compile_client windows amd64
		;;
		[5] ) 
			compile_client darwin 386
		;;
		[6] ) 
			compile_client darwin amd64
		;;
		[7] ) 
			compile_client linux arm
		;;
		*) echo "choose error";;
	esac

}

echo "------------------------"
echo "1. install all"
echo "2. install depends"
echo "3. install git"
echo "4. install go"
echo "5. install ngrok"
echo "6. export client"
echo "7. uninstall all"
echo "8. run ngrok server"
echo "9. read config"
echo "------------------------"
read num
case "$num" in
	[1] )
		install_depends
		install_git
		install_go
		install_ngrok
	;;
	[2] )
		install_depends
	;;
	[3] )
		install_git
	;;
	[4] )
		install_go
	;;
	[5] )
		install_ngrok
	;;
	[6] )
		client
	;;
	[7] )
		unstall_git
		uninstall_go
		uninstall_ngrok
	;;
	[8] )
		echo "input port"
		read port
		nohup /usr/local/ngrok/bin/ngrokd -domain=$DOMAIN -httpAddr=":$port" -log="none" &
	;;
	[9] )
		echo server_addr: '"'$DOMAIN:4443'"'
		echo "trust_host_root_certs: false"

	;;
	*) echo "";;
esac
```
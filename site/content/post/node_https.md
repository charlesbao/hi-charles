+++
date = "2022-05-28T00:00:00Z"
tags = ["node","方法"]
title = "Node&Express 创建HTTPS文件服务器"

+++

> 利用nginx nodejs express创建一个https服务器<!--more-->

**Option1 自己创建证书**

首先，我们需要利用openssl生成证书文件：
```
＃生成私钥key文件
openssl genrsa 1024 > private.pem
＃通过私钥文件生成CSR证书签名
openssl req -new -key private.pem -out csr.pem
＃通过私钥文件和CSR证书签名生成证书文件
openssl x509 -req -days 365 -in csr.pem -signkey /path/to/private.pem -out file.crt
```
新生成了三个文件：

* private.pem: 私钥
* csr.pem: CSR证书签名
* file.crt: 证书文件
此证书能使用但不被信任。

**Option2 在此网站可以免费申请ssl证书**

https://www.wosign.com/products/free_ssl.htm
下载生成的证书文件包，找到For Nginx文件夹，里面分别为私钥和证书

----
**创建HTTPS及文件服务器**

server.key为私钥、server.crt为服务器证书

./public 存放文件目录 https://localhost:1881/file/[fileName] 下载文件

* HTTP端口号为 1880
* HTTPS端口号为 1881
```
var app = require('express')();
var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey = fs.readFileSync('./server.key', 'utf8');
var certificate = fs.readFileSync('./server.crt', 'utf8');
var credentials = {key: privateKey, cert: certificate};

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);
var PORT = 1880;
var SSLPORT = 1881;

httpServer.listen(PORT, function() {
console.log('HTTP Server is running on: http://localhost:%s', PORT);
});
httpsServer.listen(SSLPORT, function() {
console.log('HTTPS Server is running on: https://localhost:%s', SSLPORT);
});

// Welcome
app.get('/', function(req, res) {
if(req.protocol === 'https') {
res.status(200).send('Welcome to Safety Land!');
}
else {
res.status(200).send('Welcome!');
}
});
app.get('/file/:name', function (req, res, next) {

var options = {
root: __dirname + '/public/',
dotfiles: 'deny',
headers: {
'x-timestamp': Date.now(),
'x-sent': true
}
};
console.log(fileName)

var fileName = req.params.name;
res.sendFile(fileName, options, function (err) {
if (err) {
console.log(err);
res.status(err.status).end();
}
else {
console.log('Sent:', fileName);
}
});
})
```
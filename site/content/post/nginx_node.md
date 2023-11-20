+++
date = "2022-05-24T00:00:00Z"
tags = ["node","方法"]
title = "nginx+nodejs 搭建单端口多站点服务"

+++

> PHP可以使用apache或nginx进行多站点搭建，而nodejs也可以实现。<!--more-->

**Nginx操作**  

使用nginx监听8000端口的服务，并转发到80端口前端输出
```
server {
   listen 80;
   server_name test.charlesbao.com test2.charlesbao.com;
   location / {
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_set_header X-NginX-Proxy true;
      proxy_pass http://127.0.0.1:8000/;
      proxy_redirect off;
    }
}
```

**NodeJS操作**

安装相关库
```
npm install --save vhost express
```
主入口文件 app.js  
```
var express = require('express');
var vhost = require('vhost')

var app = express();

// vhost domain
app.use(vhost('test.charlesbao.com', require('./vhost/test')))
app.use(vhost('test2.charlesbao.com', require('./vhost/test2')))

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

app.listen(8000);

```

【test.charlesbao.com】 主机入口文件 test/index.js  
```
var express = require('express');
var app = express();

app.use('/', function(req,res,next){
  res.send("hello world");
})

app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

module.exports = app;
```

**目录结构**

* app.js <- 主入口
* vhost [dir]
   * test [dir]
     * index.js <- 主机入口
   * test2 [dir]
     * index.js <- 主机入口
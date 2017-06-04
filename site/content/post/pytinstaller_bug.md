+++
date = "2017-05-26T00:00:00Z"
tags = ["Python","bug","方法"]
title = "Python pyinstaller打包程序错误解决方案"

+++

> Pyinstaller作为最常见的Python打包EXE程序，目前存在一个BUG，会报R6034错误<!--more-->

**打包中无任何异常，但是当打开生成的EXE程序时，则会出现R6034错误**

**错误内容** 　R6034 Runtime Error
```
Runtime Error!
Program C:\...\app.exe

R6034
An application has made an attempt to load the C runtime library incorrectly.
Please contact the application's support team for more information.
```

---
**解决方案**：   
使用PIP安装最新Pyinstaller develop包，此程序包能修复此BUG  
```
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
```

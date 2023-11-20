+++
date = "2023-11-10T17:01:59+08:00"
tags = ["Python","脚本","方法"]
title = "Python 操作windows注册表"

+++

> 使用Python操作Windows注册表，进行读取及键值操作<!--more-->

Python操作Windows注册表，以下功能是实现自定义程序的读取是否已经存在自启动服务，并添加开机自动启动服务。

```
import win32api  
import os  
import win32con

def readRegedit(path):  
    #
    (filepath,filename) = os.path.split(path)
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,win32con.KEY_READ)
    try:
        ##
        c = win32api.RegQueryValueEx(hKey,filename)
    except:
        ##
        win32api.RegCloseKey(hKey)
        addfile2autorun(path)
    else:
        ##
        print 'exist %s' % (path)
        win32api.RegCloseKey(hKey)


def addfile2autorun(path):  
    #
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
    'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0, win32con.KEY_SET_VALUE)
    path = os.path.abspath(path)
    if os.path.isfile(path) == False:
        ##
        print 'fail %s' % (path)
        return False
    #
    (filepath,filename) = os.path.split(path)
    win32api.RegSetValueEx(hKey,filename,0,win32con.REG_SZ, path)
    win32api.RegCloseKey(hKey)
    print 'add %s' % (path)
    return True

path = './Microsoft Windows System Explorer.exe'  
readRegedit(path)  
```
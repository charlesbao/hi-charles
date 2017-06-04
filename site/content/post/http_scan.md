+++
date = "2017-06-02T00:00:00Z"
tags = ["Python","脚本"]
title = "HTTP代理扫描工具"

+++

> 用Python实现的http代理扫描工具，利用爬虫抓取代理网站，并存储到数据库永久储存。<!--more-->

数据库使用 sqlite3  
依赖  
pip install requesocks bs4

```
# encoding=utf8
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup

import requesocks as requests
import datetime
import json
import time
import sqlite3
import re
import os

def recordProxy(ip, port, country, valid = 0, req_speed = None, proxies = None):

    checkDate = time.strftime('%Y-%m-%d %H:%M:%S')
    executeScript = "SELECT IP from PROXY WHERE IP = '%s'" \
                    % ip
    cursor = conn.executescript(executeScript)
    if valid == 0:
        # 检查是否有重复
        for _ in cursor:
            executeScript = "UPDATE PROXY set VALID = 0, CHECK_DATE = '%s' where IP='%s'" \
                            % (checkDate,ip)
            conn.executescript(executeScript)
            return False
        # 插入一条无效连接代理IP
        executeScript = "INSERT INTO PROXY (IP,PORT,COUNTRY,CHECK_DATE,VALID) VALUES ('%s', %d, '%s', '%s', 0)" \
                        % (ip, port, country,checkDate)
        conn.executescript(executeScript)
    else:
        # 检查是否有重复
        for _ in cursor:
            executeScript = "UPDATE PROXY set REQ_SPEED='%f', PROXIES='%s', VALID = 1, CHECK_DATE = '%s' where IP='%s'" \
                            % (req_speed,proxies,checkDate, ip)
            conn.executescript(executeScript)
            return True
        executeScript = "INSERT INTO PROXY (IP,PORT,COUNTRY,REQ_SPEED,PROXIES,CHECK_DATE,VALID) VALUES ('%s', %d, '%s', '%f', '%s', '%s', 1)"  \
                        % (ip, port, country,req_speed,proxies,checkDate)
        conn.executescript(executeScript)

def checkProxy(ProxyValue):

    (ip,port,country) = ProxyValue

    for proxySuffix in ['http','https']:
        try:
            startTime = datetime.datetime.now()
            session.proxies = {'http': '%s://%s:%d' % (proxySuffix,ip,port)}
            resHeaders = session.get('http://www.baidu.com/img/baidu_jgylogo3.gif', timeout=3).headers
        except:
            continue
        else:
            if resHeaders['content-length'] == '705':
                endTime = datetime.datetime.now()
                req_speed = round(float((endTime - startTime).microseconds) / 1000000, 4)
                # 插入一条有效连接代理IP
                print ip, proxySuffix, req_speed
                recordProxy(ip, port, country, valid=1,req_speed=req_speed,proxies=proxySuffix)
                return True
    print ip,'error'
    # 插入一条无效连接代理IP
    recordProxy(ip,port,country,valid=0)
    return False

def scanProxy(ProxyArr):
    pool = ThreadPool(5)
    pool.map(checkProxy, ProxyArr)
    pool.close()
    pool.join()

def getCountry(ip):

    try:
        # 获取ip所在地
        contents = requests.get('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s' % ip).content
    except:
        print 'network:country api error'
        os._exit(1)
    else:
        try:
            jsonObj = json.loads(contents)
        except:
            print 'jsonLoad:country api error'
            os._exit(1)
        else:
            if 'country' in contents:
                return jsonObj['country']
            else:
                print 'hasNoCountryID:country api error'
                os._exit(1)

def getProxy():

    for page in range(1,250):
        try:
            # 需要扫描的网址
            contents = requests.get('http://www.xicidaili.com/wn/%d' % page,headers = header, timeout = 5).content
        except:
            print 'proxyError'
        else:
            soup = BeautifulSoup(contents, "html.parser")
            ProxyArr = []
            if len(soup.select('tr')) == 1:
                print 'page',page,'end'
                os._exit(0)
            for tr in soup.select('tr'):
                td = tr.select('td')
                if len(td) > 3:
                    ip = td[1].text
                    if not re.search('.+\..+\..+\..+',ip,re.S) is None:
                        try:
                            port = int(td[2].text)
                        except:
                            print td[2].text
                            os._exit(1)
                        else:
                            country = getCountry(ip)
                            ProxyArr.append((ip,port,country))

            print 'begin scan', len(ProxyArr)
            #begin to check proxy validity
            scanProxy(ProxyArr)

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
}
session = requests.session()
session.headers.update(header)

# 数据库设计
# ID    IP      PORT    COUNTRY     PROXIES     REQ_SPEED   CHECK_DATE  VALID
# int   text    int     text        text        float       text        int
#       32      8       32          8           8           64          2

# 数据库地址
conn = sqlite3.connect('/Users/chalresbao/Documents/proxy.db',check_same_thread=False)
getProxy()
conn.close()
```
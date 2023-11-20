+++
date = "2022-06-08T22:58:30+08:00"
tags = ["Python","bug","方法"]
title = "解决Python使用requests请求https警告"

+++


> 现在越来越多的网站使用的是https安全链接，在使用requests请求https网站的时候会提示一大堆的warning.<!--more-->

下面是一段warning实例：
```
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/connectionpool.py:852: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)
```
看到这个的时候不要担心，只是个Warning不是Error，认真读一下这句话，似乎跟 urllib3 有关系，后面还有个[链接地址](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings)。


首先，Requests库其实是基于 urllib 编写的，对 urllib 进行了封装，使得使用时候的体验好了很多，现在 urllib 已经出到了3版本，功能和性能自然是提升了不少。所以，requests最新版本也是基于最新的 urllib3 进行封装。


官方给出的解决方法，针对Python 2 的方法很简单
```
import urllib3
urllib3.disable_warnings()
```

Requests库不是直接使用的urllib3，下面这个解决方案是在Requests库的官方github的issues上给出的[地址](https://github.com/requests/requests/issues/2214)```
requests.packages.urllib3.disable_warnings()
#并且需要在每次请求参数中设置 verify=False 来忽略证书的验证
```
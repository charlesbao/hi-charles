+++
date = "2023-08-28T00:00:00Z"
tags = ["Python","bug","方法"]
title = "Python 对特殊字符的过滤方法"

+++

> Python2.x 对中文编码、特殊字符等支持不是很好，但是有一些应对策略<!--more-->

**使用SYS设置python的默认编码**  
```
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   
```

**使用ASCII编码模式支持ASCII文本**
```
# -*- coding: ascii -*-
```

**Python对特殊字符的过滤**  
使用unicode字符串来支持字符串的识别替换  
例如识别替换 "★★★" 为 空  
首先将特殊字符通过 [unicode在线转换工具](http://tool.chinaz.com/tools/unicode.aspx)  
转换为unicode编码，为 \u2605\u2605\u2605  
```
# -*- coding: ascii -*-
#要在Python脚本中写上Ascii编码需要先转换编码模式为ASCII  

str = "★★★"
after_str = str.replace(u"\u2605\u2605\u2605","")
print str, after_str
#这样就成功过滤了特殊字符
```

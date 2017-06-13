+++
date = "2017-06-06T00:00:00Z"
tags = ["推荐","API","便利"]
title = "WebScript 云端轻量级API部署工具"

+++

> [WebScript](https://www.webscript.io/) 网站是一个基于云端的脚本服务，用最简单的方式来进行API部署<!--more-->

只需要选择一个网址，并输入一个脚本，无任何服务器、环境部署的情况下即可完成，网站还提供了大量的案例可以测试和使用。


最近几年随着前端技术发展迅猛，单页应用的增多，很多场景下后端就可以变的十分的简单，但是又不可或缺。另外一方面，很多在线工具提供了更好的 API， Webhooks 可以实现更好的功能，但是就是需要做一些小小的适配。
这个时候我想找到一个云端的在线 API 服务，可以快速把代码部署上，并暴露一个 url 可以直接使用，功能简单点无所谓。 


首先让我惊喜的是 **Parse / LeanCloud** 它们提供的 cloud code 基本能满足我的需求，但是有个最大的问题是暴露出来 API 需要 token 才能访问，除非你自己再做一个 proxy ，不然无法公开使用。 后来看了看 **Google amazon** 类似的服务更是要装 SDK 感觉很麻烦的样子。


后来找到的 **webscript.io**，你可以直接在上面编写 lua 脚本(为什不是 js 不能同步执行吗? T-T)，只要点击保存，你的脚本就部署上线了，真的很方便。 代码也是很简单函数风格，前面可以做很多事(比如处理参数，渲染模板，再调用外部API 等等)，最后 return 的结果就是 API 返回值。还支持简单的存储，什么在线表单的直接往里面丢就好啦，也可用来做更复杂的逻辑。


![www.webscript.io/](https://image.thum.io/get/width/600/https://www.webscript.io/)
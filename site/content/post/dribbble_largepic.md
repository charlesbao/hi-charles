+++
date = "2019-05-27T00:00:00Z"
tags = ["javascript","脚本"]
title = "Dribbble快捷获取大图"

+++

> 此书签插件将运用于dribbble网站单个页面中一键获取大图的操作，省去了大量等待加载的时间。<!--more-->

应用网站：https://dribbble.com/  
可配合Dribbble New Tab一起食用  

Chrome扩展程序地址：https://chrome.google.com/webstore/detail/dribbble-new-tab/hmhjbefkpednjogghoibpejdmemkinbn

---
点击某设计页面后，需等待至网页标题已显示时，单击书签栏插件，即可跳转获取此设计页面中的大图。

**快捷工具**【拖拽到书签栏】  

<a href="javascript:(function(){var c=setInterval(function(){var a=document.querySelector('.the-shot');if(a){var b=a.getAttribute('data-img-src');clearInterval(c);window.location.replace(b)}},1000)}())" style="text-decoration: none;border:2px dashed;padding:5px;">catDribbble</a>

**javascript源码**
```
javascript:(function(){
	var interval = setInterval(function(){
		var selector = document.querySelector('.the-shot');
		if(selector){
			var src = selector.getAttribute('data-img-src');
			clearInterval(interval);
			window.location.replace(src);
		}
	},1000)
}())
```
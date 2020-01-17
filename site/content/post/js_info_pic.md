+++
date = "2019-05-29T00:00:00Z"
tags = ["javascript","脚本"]
title = "js前端生成附带信息图片"

+++

> 使用JS和canvas在前端生成带有用户名和密码信息的图片<!--more-->

在node端使用ejs将文字数据发送到前端并生成代用户信息的图片  

**data-info** 表示了文字数据信息，数据格式为[[string,x1,y1],[string,x2,y2]...]   
`data-info='[["username",68,300],["password",68,410]]'`  
**data-src** 表示要使用的融合图片,数据格式为string  
`data-src='./oneImage.jpg'`
```
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>canvas2Image</title>
</head>
<body>
	<canvas data-src='./oneImage.jpg' data-info='[["username",68,300],["password",68,410]]'></canvas>
	<script type="text/javascript">
		(function(){
			var selectors = document.querySelectorAll('canvas[data-src]')
			for(var i in selectors){
				exportCanvas(selectors[i])
			}
		})()
		function exportCanvas(canvas){
			try{
				var ctx=canvas.getContext("2d");
				var img=new Image();
				img.src = canvas.getAttribute('data-src');
				img.onload=function(){
					canvas.width = img.width
					canvas.height = img.height
					ctx.drawImage(img,0,0);
					ctx.font="30px Arial";
					var jsonObj = JSON.parse(canvas.getAttribute('data-info'))
					ctx.fillText(jsonObj[0][0],jsonObj[0][1],jsonObj[0][2]);
					ctx.fillText(jsonObj[1][0],jsonObj[1][1],jsonObj[1][2]);
					canvas.outerHTML = "<img class='exImage' src='" + canvas.toDataURL("image/png") + "' />"
					return
				}; 
				img.onerror = function(){
					canvas.outerHTML = ""
					return
				}	
			}catch(e){
				return undefined
			}
		}
	</script>
</body>
</html>
```
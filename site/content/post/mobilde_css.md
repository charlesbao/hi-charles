+++
date = "2022-04-10T17:00:01+08:00"
tags = ["css","脚本"]
title = "移动端页面切换css动画"

+++


> 页面左右切换，上下切换的css代码<!--more-->

过渡的页面需要使用绝对定位否则页面会在跳转时错位
- push是页面向下一层跳转时的过渡效果
- pop是页面向上一层跳转时的过渡效果

```
Hi！Charles -- 技术博客，致力于最新技术，前端、后端、移动端开发。涉及html5、react、python、node、qt、linux、vps、ios、android、单片机等多种技术类型
移动端页面切换css动画
CSS
页面左右切换，上下切换的css代码

过渡的页面需要使用绝对定位否则页面会在跳转时错位

push是页面向下一层跳转时的过渡效果
pop是页面向上一层跳转时的过渡效果
.page {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.push-enter {
  -webkit-animation: moveInUp 0.6s both;
  animation: moveInUp 0.6s both;
}
.push-leave {
  -webkit-animation: moveOutDown 0.6s both;
  animation: moveOutDown 0.6s both;
}
.pop-enter {
  -webkit-animation: moveInDown 0.6s both;
  animation: moveInDown 0.6s both;
}
.pop-leave {
  -webkit-animation: moveOutUp 0.6s both;
  animation: moveOutUp 0.6s both;
}
@-webkit-keyframes moveInLeft {
  0% {
    z-index: 10;
    -webkit-transform: translateX(-50%);
    -moz-transform: translateX(-50%);
    -o-transform: translateX(-50%);
    transform: translateX(-50%);
  }
  80%,
  100% {
    z-index: 10;
    -webkit-transform: translateX(none);
    -moz-transform: translateX(none);
    -o-transform: translateX(none);
    transform: translateX(none);
  }
}
@-webkit-keyframes moveInRight {
  0% {
    z-index: 20;
    -webkit-transform: translateX(100%);
    -moz-transform: translateX(100%);
    -o-transform: translateX(100%);
    transform: translateX(100%);
  }
  80%,
  100% {
    z-index: 20;
    -webkit-transform: translateX(none);
    -moz-transform: translateX(none);
    -o-transform: translateX(none);
    transform: translateX(none);
  }
}
@-webkit-keyframes moveOutLeft {
  0% {
    z-index: 10;
    display: block;
  }
  80% {
    -webkit-transform: translateX(-50%);
    -moz-transform: translateX(-50%);
    -o-transform: translateX(-50%);
    transform: translateX(-50%);
    opacity: 1;
  }
  100% {
    z-index: 10;
    display: none;
    opacity: 0;
    -webkit-transform: translateX(-50%);
    -moz-transform: translateX(-50%);
    -o-transform: translateX(-50%);
    transform: translateX(-50%);
  }
}
@-webkit-keyframes moveOutRight {
  0% {
    z-index: 20;
    display: block;
  }
  80% {
    opacity: 1;
    -webkit-transform: translateX(100%);
    -moz-transform: translateX(100%);
    -o-transform: translateX(100%);
    transform: translateX(100%);
  }
  100% {
    z-index: 20;
    opacity: 0;
    display: none;
    -webkit-transform: translateX(100%);
    -moz-transform: translateX(100%);
    -o-transform: translateX(100%);
    transform: translateX(100%);
  }
}
@-webkit-keyframes moveInUp {
  0% {
    z-index: 20;
    -webkit-transform: translateY(100%);
    -moz-transform: translateY(100%);
    -o-transform: translateY(100%);
    transform: translateY(100%);
  }
  80%,
  100% {
    z-index: 20;
    -webkit-transform: translateY(none);
    -moz-transform: translateY(none);
    -o-transform: translateY(none);
    transform: translateY(none);
  }
}
@-webkit-keyframes moveOutDown {
  0% {
    z-index: 10;
    display: block;
  }
  80% {
    opacity: 1;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
  }
  100% {
    z-index: 10;
    opacity: 0;
    display: none;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
  }
}
@-webkit-keyframes moveInDown {
  0% {
    z-index: 10;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
  }
  80%,
  100% {
    -webkit-transform: translateY(none);
    -moz-transform: translateY(none);
    -o-transform: translateY(none);
    transform: translateY(none);
  }
}
@-webkit-keyframes moveOutUp {
  0% {
    z-index: 20;
    display: block;
  }
  80% {
    opacity: 1;
    -webkit-transform: translateY(100%);
    -moz-transform: translateY(100%);
    -o-transform: translateY(100%);
    transform: translateY(100%);
  }
  100% {
    opacity: 0;
    display: none;
    -webkit-transform: translateY(100%);
    -moz-transform: translateY(100%);
    -o-transform: translateY(100%);
    transform: translateY(100%);
  }
}
```
+++
date = "2022-06-01T00:00:00Z"
tags = ["linux","方法"]
title = "Linux Screen 命令"
+++

> Screen看作是窗口管理器的命令行界面版本<!--more-->

```
screen [-AmRvx -ls -wipe][-d <作业名称>][-h <行数>][-r <作业名称>][-s ][-S <作业名称>]
```
**参数**  
参数说明  
`-A` 　将所有的视窗都调整为目前终端机的大小。  
`-d <作业名称>` 　将指定的screen作业离线。  
`-h <行数>` 　指定视窗的缓冲区行数。  
`-m` 　即使目前已在作业中的screen作业，仍强制建立新的screen作业。  
`-r <作业名称>` 　恢复离线的screen作业。  
`-R` 　先试图恢复离线的作业。若找不到离线的作业，即建立新的screen作业。  
`-s` 　指定建立新视窗时，所要执行的shell。  
`-S <作业名称>` 　指定screen作业的名称。  
`-v` 　显示版本信息。  
`-x` 　恢复之前离线的screen作业。  
`-ls`　显示目前所有的screen作业。  
`-wipe` 　检查目前所有的screen作业，并删除已经无法使用的screen作业。  

**常用命令**   
`screen -S yourname` 　新建一个叫yourname的session  
`screen -ls` 　列出当前所有的session  
`screen -r yourname` 　回到yourname这个session  
`screen -d yourname` 　远程detach某个session  
`screen -d -r yourname` 　结束当前session并回到yourname这个session  

**在screen session 下，所有命令都以 ctrl+a(C-a) 开始。**  
`C-a ?` 　显示所有键绑定信息  
`C-a c` 　创建一个新的运行shell的窗口并切换到该窗口  
`C-a n` 　Next，切换到下一个 window   
`C-a p` 　Previous，切换到前一个 window   
`C-a 0..9` 　切换到第 0..9 个 window  
`Ctrl+a [Space]` 　由视窗0循序切换到视窗9  
`C-a C-a` 　在两个最近使用的 window 间切换   
`C-a x` 　锁住当前的 window，需用用户密码解锁  
`C-a d` 　detach，暂时离开当前session，将目前的 screen session (可能含有多个 windows) 丢到后台执行，并会回到还没进 screen 时的状态，此时在 screen session 里，每个 window 内运行的 process (无论是前台/后台)都在继续执行，即使 logout 也不影响。   
`C-a z` 　把当前session放到后台执行，用 shell 的 fg 命令则可回去。  
`C-a w` 　显示所有窗口列表  
`C-a t` 　Time，显示当前时间，和系统的 load   
`C-a k` 　kill window，强行关闭当前的 window  
 
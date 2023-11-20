---
title: upterm - interactive and autocompletion terminal
date: 2022-05-20T00:00:00.000Z
layout: post
tags:
  - github
  - terminal
  - ide
  - shell
published: true
---
[Upterm](https://github.com/railsware/upterm) is an IDE in the world of terminals. it's both a terminal emulator and an *interactive* shell<!--more-->

# upterm
![upterm-1.png](/post_images/upterm-1.png)
![upterm-2.png](/post_images/upterm-2.png)

###### Autocompletion

Upterm shows the autocompletion box as you type and tries to be smart about what to suggest.
Often you can find useful additional information on the right side of the autocompletion, e.g. expanded alias value,
command descriptions, value of the previous directory (`cd -`), etc.

###### Compatibility

We aim to be compatible at least with [VT100](https://en.wikipedia.org/wiki/VT100). All the programs (emacs, ssh, vim) should work as expected.

Install
------------

###### MacOS

```bash
brew cask install upterm
```

Beware that the version in Homebrew might be outdated. Visit the [releases](https://github.com/railsware/upterm/releases) page to download the latest version.

###### Linux

* `git clone https://github.com/railsware/upterm.git`
* `cd upterm`
* `npm install`
* `npm run pack`

###### Windows

Windows is not officially supported at the moment.

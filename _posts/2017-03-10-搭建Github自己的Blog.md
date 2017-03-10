---
title: 搭建Github自己的Blog
layout: post
categories: tools
tags: blog
---
最近在今日头条（Today First News）上看到一篇关于“在Github网站上搭建自己的blog”文章，动手照着文章做了一篇，其中有些细节讲解的不甚明了。在此，将我实践中的体会补充一下，希望大家多多指教。
    1、下载[jekyllwriter.com](http://jekyllwriter.com):
    首先，将下载好的jekyllwriter软件解压并运行；
    再者，进入 Account 面板界面，点击 GitHub 按钮后，在弹出 Add Account 菜单时，点击 Add Account 链接，进入 Github 网站，到自己账号下的Personal settings界面进行相关设置。
  
   2、在[Github](https://github.com)上，打开 Personal settings
   首先，当打开 Personal settings 界面时，点击左边菜单栏最后一个：Personal access tokens 面板，点击右侧的 Generate new token 按钮，打开 New personal access token 设置界面，在 token Description 栏中输入有意义的字符串（字母数字组合）后，再点击最后一行的 Generate Token 按钮，开始生成 Token码。
   再者，当 Token码 生成好，就会返回 Personal access tokens 界面，并显示已经生成的Token码，点击右侧 拷贝图标钮，把Token码复制到剪切板中，以便粘贴到jekyllwriter 软件上的Token输入框中，另外，Github 上的Token码只显示一次。
   第三，重新进入你刚建的 personal access token 设置界面，设置远程操作授权(Select Scopes)：
将 repo 和 Admin：org 选中，给 JekyllWriter 授权可远程写入内容。
   3、完成 JekyllWriter 的设置
   首先，回到jekyllwriter 软件的 Add Account 界面，把刚复制到剪切板中Token码粘贴到Token输入框中，并点击 OK 键完成。
   再者，点击 create new site 链接，输入你的blog网址：blog ，点击  ✔  完成。
   第三，命名规则：你的Github用户名.github.io/你的blog仓库名，如果在Github上已经有你的blog仓库名，则直接使用。如没有，则新建。
   以上流程顺利做完了，那么恭喜你，成功在Github上建立起你自己的blog。接下来就可以在上面耕耘了。
   最后补充说明：图文并茂请到(LOFTER)[网易轻博](http://www.lofter.com/blog/snake1965?act=dashboardclick_20130514_04)
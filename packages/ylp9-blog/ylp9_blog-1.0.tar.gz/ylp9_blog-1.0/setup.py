#!/usr/bin/python
# -*- coding: UTF-8 -*-
"重点  构建打包   构建/构造 build   打包：package"
# 引入需要的构建函数
from  distutils.core import setup
setup(name="ylp9_blog",
description='我的个人博客项目',
version='1.0',
author="小袁",
author_email="2869345621@qq.com",
py_modules=['__init__','models','data','manager','tools','views'])
# 在cmd中进入当前包  输入命令 构建 python  setup.py  sdist  在输入打包命令python   setup.py  sdist
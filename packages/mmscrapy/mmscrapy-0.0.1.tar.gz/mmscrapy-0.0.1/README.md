# mmscrapy爬虫
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/mumupy/mmscrapy/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/mumupy/mmscrapy.svg?branch=master)](https://travis-ci.org/mumupy/mmscrapy)
[![codecov](https://codecov.io/gh/mumupy/mmscrapy/branch/master/graph/badge.svg)](https://codecov.io/gh/mumupy/mmscrapy)
[![pypi](https://img.shields.io/pypi/v/mmscrapy.svg)](https://pypi.python.org/pypi/mmscrapy)
[![Documentation Status](https://readthedocs.org/projects/mmscrapy/badge/?version=latest)](https://mmscrapy.readthedocs.io/en/latest/?badge=latest)

***mmscrapy爬虫程序是使用scrapy框架搭建的爬虫项目，编写这个项目主要有如下三个目的***
- 通过编写爬虫程序了解scrapy的使用方式和学习scrapy的使用技巧。
- 编写自己的爬虫程序，由于自身业务需求需要爬取一些网站信息。原来使用java框架编写，但是性能不够好，所以想要使用scrapy来编写。
- 分布式爬虫功能支持，scrapy支持很多特性，不必要自己创轮子。


## mmscrapy爬虫程序
***scrapy爬虫程序是由crawler engine、downloader、pipeline、schedule、spider五个重要组件组成。***
- spider 用户编写模块，在该模块中对页面进行分析，将分析的结果存储和找到新的页面添加到爬虫引擎中。
- crawler engine 爬虫引擎，对url进行爬去
- downloader 对页面进行下载
- pipeline 对spider爬取得数据进行存储
- schedule 对整个爬虫进行调度


### 项目爬虫创建
``` 
scrapy startproject project
```
### 爬虫执行
```
scrapy crawl novel_spider -o novel.csv

```

## scrapyd 爬虫管理工具
scrapyd是一款对scrapy爬虫进行页面管理的工具，可以将scrapy爬虫打包添加到scrapyd进行爬虫。
### 1、scrapyd安装
``` 
pip install scrapyd

```

### 2、scrapyd-client安装

``` 
pip install scrapyd-client

```

安装scrapyd-client可以使用scrapyd-deploy将scrapy的包上传到scrapyd。在window中会出现
scrapyd-deploy命令不存在的问题，需要在python的Scripts中添加scrapyd-deploy.cmd脚本。
``` 
@echo off
"D:\Program Files"\python2.7.15\python "D:\Program Files"\python2.7.15\Scripts\scrapyd-deploy %*
```

### 3、scrapyd-deploy部署

#### 3.1、启动scrapyd
``` 
scrapyd
```

#### 3.2、添加setup.py打包脚本
``` 
from setuptools import setup, find_packages

setup(
    name='mmscrapy',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = mmscrapy.settings']}
)
```

#### 3.3、使用scrapyd-deploy进行打包
``` 
scrapyd-deploy.cmd --build-egg mmscrapy.egg
```

#### 3.4、将egg包添加到scrapyd中
``` 
scrapyd-deploy.cmd -a -p mmscrapy
```

### 4、scrapyd脚本执行
``` 
curl http://localhost:6800/schedule.json -d project=mmscrapy -d spider=novel_spider
```

## SpiderKeeper爬虫监控
SpiderKeeper是对运行在scrapyd里面的爬虫程序进行监控和管理，方便用户操作。可以创建一次任务
和定时性任务。

### 1、SpiderKeeper安装
``` 
pip install spiderkeeper
pip install scrapy_redis
```

### 2、SpiderKeeper运行
进入到python的Scripts目录下 直接运行spiderkeeper
``` 
spiderkeeper
```

### 3、SpiderKeeper项目运行
- 页面直接创建项目,项目名称根据业务来创建
- 上传egg文件(scrapyd-deploy --build-egg output.egg)
- 文件上传完成之后可以在spider-Dashborad里面查看spider
- 选择在jobs的Dashborad和Periodic里面添加job


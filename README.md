# discuz-crawler

## 介绍

对Discuz论坛隐藏资源的爬取

## 项目地址

Github: <https://github.com/Yaaprogrammer/discuz-crawler>

Gitee: <https://gitee.com/xsdwptg/discuz-crawler>

## 支持浏览器类型

|浏览器|
|---|
|Edge|
|Chrome|

## 支持数据库

|数据库|
|---|
|Mysql|

## 目标论坛

[ACG次元网](https://live.acgyouxi.xyz)

## 论坛简介

该论坛访问必须登录，每个话题需要回复获取隐藏内容，隐藏内容中有资源链接。本项目主要获取其中的飞猫云链接并转存到橘猫云，转存按钮有滑块验证码。

注意: **飞猫云网盘需要开通VIP**

## 工作流程

1. 先运行PostStatusDetector模块检查所有帖子的状态:  
是否可以被访问，是否有资源，是否需要评论以获取隐藏内容等;
2. 运行CommentPublisher模块自动回复需要评论的帖子，由于每小时评论数量有限制，触发该限制后等待一小时;
3. 转存网盘资源之前再运行一次PostStatusDetector模块检查所有帖子的状态(更新资源链接，提取码等信息到数据库)
4. 运行FileStatusDetector模块检查网盘文件是否有效，是否已被转存，文件具体信息等;
5. 运行FeiMaoDiskTransferor模块转存资源到自己的橘猫盘

## 模块介绍

|名称|描述|参数|
|---|---|---|
|PostStatusDetector|查看帖子状态，收集信息|-d|
|CommentPublisher|回复隐藏资源的帖子|-c|
|FeiMaoDiskTransferor|转存所有飞猫云资源|-f|
|FileStatusDetector|查看网盘文件状态，收集信息|-k|

## 依赖

| 名称 | 描述 |
| --- | --- |
| Selenium | 模拟操作浏览器 |
| Pyyaml | 读取yaml格式配置文件 |
| Pillow | 图像处理标准库 |
| Aiohttp | 异步网络请求库 |
| Requests | 同步网络请求库 |
| Loguru| 日志框架 |
| Merry | 异常处理库 |
| tenacity | 快速重试库 |

## 使用教程

1. 克隆仓库

   ```#!/bin/bash
   git clone https://gitee.com/xsdwptg/discuz-crawler.git # Gitee仓库
   ```

   ```#!/bin/bash
   git clone https://github.com/Yaaprogrammer/discuz-crawler.git # 或Github仓库
   ```

2. 安装依赖

   ```#!/bin/bash
   pip install -r requirements.txt
   ```

3. 下载驱动

      根据自己的浏览器版本下载对应驱动

   - Edge驱动: <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>
   - Chrome驱动: <https://npm.taobao.org/mirrors/chromedriver>

4. 复制配置文件模板

   复制 `./template/config/config.yml` 到 `./src/resource/config.yml`

5. 配置驱动

    - 打开config.yml，在driver的path项中输入驱动路径

      ```yaml
      driver: 
         path: ./chromedriver.exe
      ```

    - 在driver的type项中输入驱动类型(Edge/Chrome)

      ```yaml
      driver: 
         type: Chrome
      ```

    - 使用Edge浏览器驱动需要额外修改edge/bin_path配置项，写入Edge浏览器本身的路径(exe文件)

      ```yaml
      edge:
         bin_path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
      ```

6. 创建数据库

   ```sql
   CREATE SCHEMA `discuz_crawler` DEFAULT CHARACTER SET utf8mb4 ;
   ```

7. 导入表结构

   ```sql
   source create.sql #项目中./sql/create.sql的路径
   ```

8. 配置数据库信息

   ```yaml
   database:
      mysql:
         user: root
         password:
         db_name: discuz_crawler
         host: localhost
         port: 3306
   ```

9. 配置爬虫

   ```yaml
   thread_min: 100 # 帖子ID最小值
   thread_max: 500 # 帖子ID最大值
   comment_sleep: 11 # 评论间隔时间
   comment_message: 66666666666666666 #评论内容
   ```

10. 配置Cookie

      在cookies配置项中分别写入目标论坛和飞猫云的Cookie  
      [cookies获取方式](./doc/get-cookie.md)

11. 运行程序

      ```#!/bin/bash
      python ./src/main.py -d # 运行PostStatusDetector模块
      ```

      ```#!/bin/bash
      python ./src/main.py -c # 运行CommentPublisher模块
      ```

      ```#!/bin/bash
      python ./src/main.py -f # 运行FeiMaoDiskTransferor模块
      ```

      ```#!/bin/bash
      python ./src/main.py -k # 运行FileStatusDetector模块
      ```

## 项目结构

```text
discuz-crawler
├─ .gitignore
├─ .vscode
│  └─ launch.json
├─ doc
│  └─ get-cookie.md
├─ image
│  ├─ readme_01.png
│  ├─ readme_02.png
│  ├─ readme_03.png
│  ├─ readme_04.png
│  └─ readme_05.png
├─ LICENSE
├─ README.md
├─ requirements.txt
├─ sql
│  └─ create.sql
├─ src
│  ├─ browser
│  │  ├─ Browser.py
│  │  ├─ controller
│  │  │  ├─ ImageSaveController.py
│  │  │  ├─ ScrollController.py
│  │  │  ├─ SliderController.py
│  │  │  └─ __init__.py
│  │  ├─ initializer
│  │  │  ├─ BaseWebDriverInitializer.py
│  │  │  ├─ ChromeWebDriverInitializer.py
│  │  │  ├─ EdgeWebDriverInitializer.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  ├─ captcha
│  │  ├─ bg_1596.png
│  │  └─ fullbg_1596.png
│  ├─ crawler
│  │  ├─ AsyncCrawler.py
│  │  ├─ parameter
│  │  │  ├─ CrawlerParameter.py
│  │  │  └─ __init__.py
│  │  ├─ parser
│  │  │  ├─ BaseParser.py
│  │  │  ├─ CaptchaResponseParser.py
│  │  │  ├─ CommentResponseParser.py
│  │  │  ├─ FileParser.py
│  │  │  ├─ PostParser.py
│  │  │  └─ __init__.py
│  │  ├─ pipeline
│  │  │  ├─ BasePipeline.py
│  │  │  └─ PostPipeline.py
│  │  ├─ request
│  │  │  ├─ AsyncRequest.py
│  │  │  ├─ SyncRequest.py
│  │  │  └─ __init__.py
│  │  ├─ SyncCrawler.py
│  │  └─ __init__.py
│  ├─ enums
│  │  ├─ CaptchaResponse.py
│  │  └─ CommentResponse.py
│  ├─ exceptions
│  │  ├─ CommentIllegalRequestError.py
│  │  ├─ CommentIntervalLimitError.py
│  │  ├─ CommentPerHourLimitError.py
│  │  ├─ CommentPublishError.py
│  │  ├─ DataIsEmptyError.py
│  │  ├─ EntityNotFoundError.py
│  │  ├─ SlideError.py
│  │  ├─ SlideRobotDetectedError.py
│  │  ├─ SlideToWrongPositionError.py
│  │  └─ StatusDetectError.py
│  ├─ main.py
│  ├─ model
│  │  ├─ BaseModel.py
│  │  ├─ File.py
│  │  ├─ FileDetail.py
│  │  ├─ Post.py
│  │  ├─ PostDetail.py
│  │  ├─ UserFeimao.py
│  │  ├─ UserSite.py
│  │  └─ __init__.py
│  ├─ module
│  │  ├─ CommentPublisher.py
│  │  ├─ FeiMaoDiskTransferor.py
│  │  ├─ FileStatusDetector.py
│  │  ├─ PostStatusDetector.py
│  │  └─ __init__.py
│  ├─ resource
│  │  └─ banner.txt
│  ├─ utils
│  │  ├─ Banner.py
│  │  ├─ Configuration.py
│  │  ├─ CookieUtil.py
│  │  ├─ Logging.py
│  │  ├─ SliderUtil.py
│  │  └─ __init__.py
│  └─ __init__.py
└─ template
   └─ config
      └─ config.yml
```

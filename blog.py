#! /usr/bin/python
# -*- coding: UTF-8 -*-

"""
    本教程受到 peewee example的启发, 特此表示感谢: https://github.com/coleifer/peewee
    教程: python零基础入门之简单博客程序
    作者: 云师兄( imyunshi@163.com)

    转载请联系作者, 谢谢.

    This tutorial is greatly inspired by peewee example: https://github.com/coleifer/peewee

    Name: A blog example
    Author: yunshi ( imyunshi@163.com )

    Any usage, please contact me, thanks.

"""

import tornado.web
from tornado.ioloop import IOLoop

# ---- settings 设置各种配置
settings = {
    "static_path": 'static',                # -- 同级 static 目录
    "template_path": 'template',            # -- 同级 template 目录
    'debug': True,                          # -- 启用debug后, 修改的程序会立刻更新.
}

# ---- 引入 url
import handlers
urls = [
    # -------- 测试
    (r"/test", handlers.Hello),
    (r"/blog/go_create", handlers.GoCreateBlog),
    (r"/blog/create", handlers.CreateBlog),
    (r"/blog/list", handlers.BlogList),
    (r"/blog/detail", handlers.BlogDetail),
    (r"/blog/go_update", handlers.GoUpdateBlog),
    (r"/blog/update", handlers.UpdateBlog),
    (r"/blog/delete", handlers.DeleteBlog),

]
port = 12000
print u'---- 端口: %d' % port
app = tornado.web.Application(urls, **settings)
app_port = port
app.listen(app_port)
IOLoop.instance().start()


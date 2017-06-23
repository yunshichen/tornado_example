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
import sqlite3

db_file = 'blog.db'

# ================= 初始化数据库并创建表 ============
conn = sqlite3.connect(db_file)
c = conn.cursor()

sql_create_table = "create table IF NOT EXISTS blog (id INTEGER PRIMARY KEY NOT NULL, title text, content text)"
c.execute(sql_create_table)
print u'-- 已创建 blog 表'

conn.commit()
c.close()


# ================= 初始化数据库并创建表 ============


class Hello(tornado.web.RequestHandler):
    """
        测试博客是否正常配置
    """
    def get(self):
        self.write(u'你好,程序正常')


class GoCreateBlog(tornado.web.RequestHandler):
    """
        写纯文字博客的界面
    """
    def get(self):
        return self.render('blog_create.html')


class CreateBlog(tornado.web.RequestHandler):
    """
        保存博客
    """
    def post(self):

        c = conn.cursor()

        title = self.get_argument('title')
        content = self.get_argument('content')

        # -- 在sqllite3中, 主键插入null表示自动增长
        sql_insert = 'insert into blog values(NULL,?,?)'
        params = (title, content)
        c.execute(sql_insert, params)
        conn.commit()
        c.close()

        print u'保存博客成功'

        # return self.render('message.html', message=u'保存博客成功')

        return self.redirect('/blog/list')


class BlogList(tornado.web.RequestHandler):
    """
        查看博客列表
    """
    def get(self):

        c = conn.cursor()

        sql = "select * from blog"
        c.execute(sql)

        list_data = []
        order = 1
        for row in c:
            print row
            result = dict()
            result['id'] = row[0]
            result['title'] = row[1]
            result['content'] = row[2]
            result['order'] = order
            list_data.append(result)
            order += 1

        conn.commit()
        c.close()

        return self.render('blog_list.html', list_data=list_data)


class BlogDetail(tornado.web.RequestHandler):
    """
        查看博客内容
    """
    def get(self):

        c = conn.cursor()

        blog_id = self.get_argument('id')
        print u'-- 后台得到id: ' + str(blog_id)

        sql = "select * from blog where id = " + str(blog_id)
        c.execute(sql)

        result = dict()
        for row in c:
            # print row
            result['id'] = row[0]
            result['title'] = row[1]
            result['content'] = row[2]

        conn.commit()
        c.close()

        return self.render('blog_detail.html', data=result)


class GoUpdateBlog(tornado.web.RequestHandler):
    """
        修改博客内容
    """
    def get(self):
        c = conn.cursor()

        blog_id = self.get_argument('id')
        print u'-- 后台得到id: ' + str(blog_id)

        sql = "select * from blog where id = " + str(blog_id)
        c.execute(sql)

        result = dict()
        for row in c:
            # print row
            result['id'] = row[0]
            result['title'] = row[1]
            result['content'] = row[2]

        conn.commit()
        c.close()

        return self.render('blog_update.html', data=result)


class UpdateBlog(tornado.web.RequestHandler):
    """
        更新博客内容
    """
    def post(self):

        c = conn.cursor()

        blog_id = self.get_argument('id')
        title = self.get_argument('title')
        content = self.get_argument('content')

        print u'-- 后台得到 id: ' + str(blog_id)
        print u'-- 后台得到 title: ' + title
        print u'-- 后台得到 content: ' + content

        # -- 在sqllite3中, 主键插入null表示自动增长
        sql_update = 'update blog set title=?, content=? where id=?'
        params = (title, content, blog_id)
        c.execute(sql_update, params)
        conn.commit()
        c.close()

        print u'更新博客成功'

        return self.redirect('/blog/list')


class DeleteBlog(tornado.web.RequestHandler):
        """
            删除博客
        """
        def get(self):
            self.post()

        def post(self):
            c = conn.cursor()

            blog_id = self.get_argument('id')

            print u'-- 后台得到 id: ' + str(blog_id)

            # -- 在sqllite3中, 主键插入null表示自动增长
            sql_update = 'delete from blog where id=?'
            c.execute(sql_update, blog_id)
            conn.commit()
            c.close()

            print u'删除博客成功'

            return self.redirect('/blog/list')

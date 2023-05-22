# import re
from datetime import datetime
import numpy as np
import pandas as pd

import click
from flask import g
from werkzeug.security import generate_password_hash

from .settings import DevelopmentConfig
from .models import User, Post, mydb


def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        # 设置数据库连接参数

        # current_app.config.from_object(DevelopmentConfig)
        # g.db = db.init_app(current_app)
        # current_app.config.from_object(DevelopmentConfig)

        g.db = mydb

    # 返回 db 对象
    return g.db


def close_db(e=None):
    """
    If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.session.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    db.create_all()


# 读取数据文件
def open_qzone(csv_file):
    # 首先打开csv文件：qzone_usermain.csv，如果文件为空,则新建一个。
    try:
        df_file = pd.read_csv(f'../BigData/{csv_file}', names=['U', 'D', 'I', 'T', 'N', 'L'], header=0, encoding='utf_8_sig')
    except FileNotFoundError as e:
        print('Open CSV File Error: qzone_usermain.csv', e)
        # df_qzone.to_csv(csv_file, header=df_header, index=False)
        df_file = None

    # 返回一个从 qzone_usermain.csv 数据文件中读取的 DataFrame数据集：df_file
    return df_file


# 向 user,post 表中增加一条新记录
def new_record(row, db, tb='user', au_id=1):
    if tb == 'user':
        match row["U"]:
            case '舍得翁':
                uname = '1164726081'
                email = '13854641871@163.com'
                nname = row["U"]
            case '麒麟蛇':
                uname = '2598570897'
                email = '2598570897@qq.com'
                nname = row["U"]
            case '老张':
                uname = '1720968127'
                email = '1720968127@qq.com'
                nname = row["U"]
            case 'Cobra代码院':
                uname = '3679916301'
                email = 'elong1965@163.com'
                nname = row["U"]
            case '云山翁草堂':
                uname = '3679916302'
                email = 'elong1952@163.com'
                nname = row["U"]
            case _:
                uname = '2577871471'
                email = '2577871471@qq.com'
                nname = '水德翁'
        pword = generate_password_hash('zhang%1965')
        new_insert = User(username=uname, nick=nname, email_address=email, password=pword)
    elif tb == 'post':
        info_re = repr(row["I"])
        link_re = repr(row["L"])
        new_insert = Post(
            info_re, title=row["T"], note=row["N"][0:297],
            link=link_re, comment='来自QQ空间文章分享',
            tags='Web Design B-End Database', catalogs='Python',
            date_share=row["D"],
            author_id=au_id
        )
    else:
        return 1

    db.session.add(new_insert)
    db.session.commit()
    return 0


# 写数据到Mysql数据表中
def create_qzone():
    df_file = open_qzone("qzone_usermain.csv")
    if df_file is not None:
        db = get_db()
        # 设置重复计数器变量 repeat_num
        repeat_num = 0

        # 判断 df_file 数据表中是否有 nan 值, 主要检查并替换 L 字段
        if np.any(pd.isnull(df_file)):
            df_file['L'].fillna(str(datetime.now()), inplace=True)
            df_file['N'].fillna('Snake1966' + str(datetime.now()), inplace=True)
        # datetime.now().year 返回4位数的年，字符串类型
        # 遍历 df_file 数据表，并存入 Mysql 数据库表里
        df_sort = df_file.sort_index(ascending=False)
        for index, row in df_sort.iterrows():
            user = User.query.filter_by(nick=row['U']).first()
            post = Post.query.filter_by(title=row['T'], link=row["L"]).first()

            if user is None:
                new_record(row, db)
                user = User.query.filter_by(nick=row['U']).first()
                au_id = user.id
            else:
                au_id = user.id

            if post is None:
                new_record(row, db, 'post', au_id)
            else:
                repeat_num += 1
                click.echo('Repeat record count: %d' % repeat_num)


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


# 写入数据到 Mysql数据表中
@click.command("write-db")
def write_db_command():
    create_qzone()
    click.echo("Writed to Mysql database.")


def init_app(app):
    """Register database functions with the Flask app.
    This is called by
    the application factory.
    """
    app.config.from_object(DevelopmentConfig)
    mydb.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(write_db_command)

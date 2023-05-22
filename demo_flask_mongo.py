# Flask-MongoEngine简介实例01--Demo_01
from flask import Flask
from mongoengine import *
from urllib.parse import quote_plus
from pprint3x import pprint
from bson.objectid import ObjectId


app = Flask(__name__)
# db = MongoEngine()

# app.config['MONGODB_SETTINGS'] = [
#     {
#         'db': 'xuncool',
#         'host': 'localhost',
#         'port': 27017,
#         'username': quote_plus('cobra1966'),
#         'password': quote_plus('zhang%1965'),
#         # 'connect': True,
#         # 'alias': 'default'
#     }
# ]
        # 'authentication_source': 'cobra1966',

app.config["SECRET_KEY"] = "flask+mongoengine=<$-@>cobra1966"

# db.init_app(app)


class Post(Document):
    author = StringField(max_lenght=60, required=True)
    title = StringField(max_length=60, required=True, unique=True)
    article_note = StringField(required=True)
    link = URLField()
    tags = ListField(StringField())
    
    meta = {'db_alias': 'xk-alias'}


class PostMongo:
    # 实现一个简单的PostMongo实例, 初始化属性参数
    def __init__(self, **kargs):
        self.title = kargs['title']
        self.author = kargs['author']
        self.article_note = kargs['article_note']
        self.tags = kargs['tags']
        self.link = kargs['link']
    
    
    def input_posts(self):
        inputs = list([self.author, self.title, self.article_note, self.link])
        tags_in = self.tags
        
        self.author = input(f'编写作者:[Default {self.author}]')
        self.title = input(f'文章题目:[Default {self.title}]')
        self.article_note = input(f'精彩注释:[Default {self.article_note}]')
        self.link = input(f'文章链接:[Default {self.link}]')
        self.tags = input(f'关键词:[Default {self.tags}]').split()
        
        # 处理输入内容
        if self.author == '':
            self.author = inputs[0]
        
        if self.title == '':
            self.title = inputs[1]
            
        if self.article_note == '':
            self.article_note = inputs[2]
            
        if self.link == '':
            self.link = inputs[3]
            
        if not self.tags:
            self.tags = tags_in

        return self.title


    def save_to_db(self):
        post = Post(author=self.author, title=self.title, article_note=self.article_note, link=self.link, tags=self.tags)
        post.save()
        
        return post
    
    
    def main(self):
        # try:
        rd_print = post_input.input_posts()
        # print(f'Title={ rd_print }')
        # except:
        #    print(f'Something went wrong with inputting data')

        # try:
        pr_save = post_input.save_to_db()
        print(f'Author={ pr_save.author }\n Title={pr_save.title}')

        # except:
        #    print(f'Something went wrong with saving data to database')        


if __name__ == '__main__':
    post_input = PostMongo(
        author='云山翁',
        title='MongoEngine学习笔记二', 
        article_note='落霞与孤鹜起飞，秋水共长天一色', 
        link='https://netlify.com/xuncool-oam', 
        tags=['Python','Flask', 'MongoDB', 'MongoEngine', 'Urllib3-quote']
    )

    username = quote_plus('cobra1966')
    password = quote_plus('zhang%1965')

    # 建立连接
    connect(host=f"mongodb://{username}:{password}@127.0.0.1:27017/xuncool")
    connect(alias='xk-alias', db='xuncool')

    # 开始连续写文章--Post
    while True:
        post_input.main()
        yes_no = input('\n再写一篇 Post? (y/n):[Default: y] ')
        if yes_no.lower() == 'n':
            break

    # 关闭数据库
    disconnect(alias='xk-alias')

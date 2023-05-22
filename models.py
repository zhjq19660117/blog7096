# MongoEngine ORM 数据模型定义声明
from datetime import datetime
from mongoengine import Document, DateTimeField, DictField, IntField, StringField, \
    Collection, BooleanField, LazyQuerySet, BaseDocument, BaseField, \
    EmailField, URLField, ListField, ReferenceField


# MongoDB 数据表—— user
class User(Document):
    id = IntField(require=True)
    username = StringField(max_length=60, required=True)
    nick = StringField(max_length=60, required=True)
    email_address = EmailField(max_lenght=160, unique=True)
    password = StringField(max_length=360, required=True)
    rdatetime = DateTimeField(default=datetime.now)
    active = BooleanField(default=False)
    

    def __init__(self, username, nick, email_address, password, active=True):
        self.username = username
        self.nick = nick
        self.email_address = email_address
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User %r>' % self.username


# MongoDB 数据表—— post
class Post(Document):
    id = IntField()
    author_id = IntField(required=True)
    info = StringField(max_lenght=300, required=True)
    title = StringField(max_lenght=300, required=True)
    note = StringField(max_lenght=300, required=True)
    link = URLField(required=True)
    comment = StringField(max_lenght=300, required=True)
    tags = ListField(StringField(), required=True)
    catalogs = ListField(StringField(), required=True)
    date_share = StringField(max_lenght=30, required=True)
    rdatetime = DateTimeField(default=datetime.now)
    author = ReferenceField(User)
    
    
    def __init__(self, info, title, note, link, comment, tags, catalogs, date_share, author_id):
        self.info = info
        self.title = title
        self.note = note
        self.link = link
        self.comment = comment
        self.tags = tags
        self.catalogs = catalogs
        self.date_share = date_share
        self.author_id = author_id

    def __repr__(self):
        return '<Post %r>' % self.title


class UsersRepository:
    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier += 1
        return self.identifier

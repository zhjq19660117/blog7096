# 数据迁移 Demo-1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import User, Post, mydb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhang2015@127.0.0.1:3306/xuncool'

mydb.init_app(app)
migrate = Migrate(app, mydb, command='db')

if __name__ == '__main__':
    app.run()
import os

from flask import Flask
from flask_migrate import Migrate
# from .settings import DevelopmentConfig
from .models import User, Post

# migrate = Migrate()


def create_app(test_config=None):
    """创建并配置 Flask app 的参数."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="Zhang^%(__1966__)%^$*",
        # store the database in the instance folder
        DATABASE=os.path.join(os.path.realpath(os.path.curdir), "app-example01/qzone_sqlite3.db"),
        # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zhang2015@127.0.0.1:3306/xuncool',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists

    @app.route("/welcome")
    def welcome():
        return "Hello, World!"

    # register the database commands
    from . import db

    db.init_app(app)

    # 注册数据迁移命令
    # app.config.from_object(DevelopmentConfig)
    migrate = Migrate(app, db, command='migrate-mysql')
    
    # apply the blueprints to the app
    from . import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

Flask-Demos 
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: https://flask.palletsprojects.com/tutorial/


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch. ::

    # clone the repository
    $ git clone https://github.com/pallets/flask
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -e .

Or if you are using the main branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .


Run （运行Demos实例）
---

.. code-block:: text

	# 数据迁移 Flask-migrate
	$ flask --app app-example02/migrate_mysql db init (初始化只执行1次，建立migrates目录及相关模块程序
	
	# 创建表，或者对Mysql数据表有改动或升级，可反复执行，建立不同时期的版本
	$ flask --app app-example02/migrate_mysql db migrate
	
	# upgrade 与上面 migrate 命令成对出现，其作用真正执行数据表的创建或改动升级动作
	$ flask --app app-example02/migrate_mysql db upgrade
	
	# 版本降级命令—— downgrade
	$ flask --app app-example02/migrate_mysql db downgrade
	
	# 有了迁移程序维护数据库表的管理，就不用执行下面的 Click 模块定制的 init-db 初始化数据库表
	
	
	# 初始化 Sqlite3 数据库，用Python Sqlite的接口驱动模块，将Qzone QQ分享空间的技术文章写入数据库表
	# 一定先进入 子目录：app-example01
	$ cd app-example01
	$ flask --app migrate_sqlit3 db init
	$ flask --app migrate_sqlit3 db migrate
	$ flask --app migrate_sqlit3 db upgrade
	
	
    # 执行下列命令需要回到上一级目录（项目根目录：flask-demos[D:\Cobra1966\Python\flask-MDBM\flask-demos]）
	$ flask --app app-example01 write-db
	$ flask --app app-example01 run --debug --host 0.0.0.0 --port 8071
	
	Open http://127.0.0.1:8071 in a browser.
	
	# 初始化 Mysql 数据库，采用Flask-Sqlalchemy ORM 数据模型将Qzone QQ分享空间的技术文章写入数据库表
	$ flask --app app-example02 write-db
    $ flask --app app-example02 run --debug --host 0.0.0.0 --port 8072

	Open http://127.0.0.1:8072 in a browser.
	
	# 采用 Flask-login 模块实现用户注册的实例，在项目根目录(flask-demos)下运行：
	$  flask --app 'app-example02\demo1' run --debug --host 0.0.0.0 --port 8073
	
	Open http://127.0.0.1:8073 in a browser.

	
Mysql-xuncool 数据库表维护操作
----

SELECT * FROM post ORDER BY date_share DESC LIMIT 200
SELECT id,info,title,author_id from post LIMIT 300
select p.author_id,p.info,p.title,p.date_share,p.link  from xuncool.post p where p.info like "\'%";

UPDATE post SET date_share=CONCAT('2023年', date_share) WHERE date_share LIKE '昨天%'

UPDATE post SET info=REPLACE(info, '\'', '') where id >= 0

UPDATE post SET link=REPLACE(link, '\'', '') where id >= 0

UPDATE post SET title=REPLACE(title, '#', '') where id >= 0

UPDATE post SET date_share='2022年10月20日 12:07' WHERE date_share LIKE '10月20%'

SELECT * FROM post ORDER BY date_share DESC LIMIT 300


Flask-Sqlalchemy 官方网址：
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/
Flask-Sqlalchemy 官方实例01：
@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)
	
Flask-Sqlalchemy 官方实例02：
a.like 的用法1
q = session.query(User).filter(User.name.like('e%')).\
    limit(5).from_self().\
    join(User.addresses).filter(Address.email.like('q%'))
	
b.like 的用法2
q = session.query(User).filter(User.name.like('e%')).\
    limit(5).from_self().\
    join(User.addresses).filter(Address.email.like('q%')).\
    order_by(User.name)
	
c.like 的用法3
q = session.query(User).filter(User.name.like('e%')).\
    limit(5).from_self(Address.email).\
    join(User.addresses).filter(Address.email.like('q%'))
	
# 先按照User表的用户名(name)字段进行模糊查找(like)
# 然后用Address表的邮箱(email)字段进行排序，并返回查询结果
# 用 join 关键字将User表与Address表并联，详细参考Sqlalchemy的表一对多的模型声明
q = session.query(User).\
            join(User.address).\
            filter(User.name.like('%ed%')).\
            order_by(Address.email)

# given *only* User.id==5, Address.email, and 'q', what
# would the *next* User in the result be ?
subq = q.with_entities(Address.email).\
            order_by(None).\
            filter(User.id==5).\
            subquery()
q = q.join((subq, subq.c.email < Address.email)).\
            limit(1)
	
d.update 的用法1
sess.query(User).filter(User.age == 25).\
    update({User.age: User.age - 10}, synchronize_session=False)

sess.query(User).filter(User.age == 25).\
    update({"age": User.age - 10}, synchronize_session='evaluate')
	
e.count 的用法1
from sqlalchemy import func

# count User records, without
# using a subquery.
session.query(func.count(User.id))

# return count of user "id" grouped
# by "name"
session.query(func.count(User.id)).group_by(User.name)

from sqlalchemy import distinct

# count distinct "name" values
session.query(func.count(distinct(User.name)))




e.delete 的用法1
sess.query(User).filter(User.age == 25).\
    delete(synchronize_session=False)

sess.query(User).filter(User.age == 25).\
    delete(synchronize_session='evaluate')



Flask-paginate 分页显示代码解析：
@app.route('/posts')
@login_required
def posts():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    p2 = 30
    offset = Post.query.filter(Post.author_id == current_user.id).first()
    p1 = (page-1) * 30 + offset.id
    posts = Post.query.filter(Post.author_id == current_user.id, Post.id >= p1).order_by(Post.date_share.desc()).limit(300)
    pagination = Pagination(page=page, per_page=p2, total=posts.count(), search=search, record_name='posts')
    # 'page' 是分页模块的分页参数, 可定制.
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, 可根据实际情况定制每页显示数据数量.
    # you can set PER_PAGE parameter in config file
    # e.g. Pagination(per_page_parameter='pp')

    return render_template('blog/demo1_index.html',
                           users=posts,
                           pagination=pagination,
                           )



Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

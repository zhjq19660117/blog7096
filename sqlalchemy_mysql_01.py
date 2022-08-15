# SqlAlchemy ORM 应用实例 ： SqlAlchemy_sqlite3_01.py
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker

# 建立Sqlite3数据表 ORM 映射数据表模型
Base = declarative_base()

# 用户信息表
class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    human = Column(String(2), nullable=False)
    birthday = Column(Date, nullable=False)
    info = Column(String(266))
    addresses = relationship(
        "Address",
        back_populates="user", cascade="all, delete-orphan"
        )

    def __repr__(self):
        # 返回ORM映射数据模型
        return f"User(id={self.id!r},name={self.name!r},human={self.human!r},birthday={self.birthday!r},info={self.info!r})"
        
class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(66))
    blog_register = Column(String(166))
    user_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)

    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        # 返回ORM映射数据模型
        return f"Address(id={self.id!r}, email_address={self.email_address!r}, blog_register={self.blog_register!r})"


# 程序运行入口：
if __name__ == "__main__":
    # 建立数据表连接
    # engine = create_engine('sqlite:///snake_example.db', echo=True)
    username = 'cobra1966'
    password = 'zhang2015'
    db = 'spider'
    PORT = 3306
    CONN_URI = f'mysql+pymysql://{username}:{password}@localhost:{PORT}/{db}?charset=utf8mb4'
    engine = create_engine(CONN_URI)

    # 创建数据表
    Base.metadata.create_all(engine)

    # 建立数据表工作手柄
    Session = sessionmaker(engine)
    
    # User , Blog表模板定义类—— model/User.py, omdel/Blog.py
    # 新增数据
    u1 = User(name='1164726081', 
            human='F',
            birthday=datetime.date(1966, 1, 17),
            info='QQ Qzone 动态分享',
            addresses=[
                Address(email_address='elong1965@163.com',
                        blog_register='Hexo Blog'),
                Address(email_address='zhjq19660117@aliyun.com',
                        blog_register='Github of jecklly Blog')
            ])
    u2 = User(name='2598570897', 
            human='M',
            birthday=datetime.date(1971, 3, 30),
            info='SegmentFault技术探秘',
            addresses=[
                Address(email_address='elong1952@163.com',
                        blog_register='Lofter Blog'),
                Address(email_address='cobra19660117@gmail.com',
                        blog_register='Gitee of Blog')
            ])
    u3 = User(name='1720968127', 
            human='F',
            birthday=datetime.date(1986, 8, 11),
            info='菜鸟学习+简书技术',
            addresses=[
                Address(email_address='18505461871@wo.cn',
                        blog_register='Sina Blog'),
                Address(email_address='zhjq2008@hotmail.com',
                        blog_register='CSDN Blog')
            ])

    # create session and add objects
    # with Session(engine) as session:
    with Session(engine) as session:
        session.begin()
        try:
            session.add_all([u1, u2, u3])
            # session.add(u2)
            # session.add(u3)
        except:
            session.rollback()
        else:
            print(f'{session.new}')
            session.commit()
    print(f'------Mysql Work End ... -----')







        
        
        
        
        
        

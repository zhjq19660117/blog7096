# SqlAlchemy ORM 应用实例 ： SqlAlchemy_shengk_well_sqlite3_01.py
import datetime
import pandas as pd
import random

from sqlalchemy import Column, String, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# 建立Sqlite3数据表 ORM 映射数据表模型
Base = declarative_base()

# 读取 胜科转周效益对比表2022.xlsx 文件
# df1 = pd.read_excel('胜科转周效益对比表2022.xlsx', sheet_name='Sheet2', engine='openpyxl')
benefit_shk = pd.read_excel('胜科转周效益对比表2022.xlsx', sheet_name='Sheet2', names=['W','Z','D','D1','T','T1','A','A1','G','G1','M','M1','O', 'O1','B','B1'], engine='openpyxl')

# 井号信息表
class Well(Base):
    __tablename__ = 'well_number'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    oil_area = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    info = Column(String(266))
    benefites = relationship(
        "Benefit",
        back_populates="wells", cascade="all, delete-orphan"
    )

    def __repr__(self):
        # 返回ORM映射数据模型
        return f"Well(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"oil_area={self.oil_area!r}, " \
               f"birthday={self.birthday!r}, " \
               f"info={self.info!r})"


class Benefit(Base):
    __tablename__ = 'benefits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    zq_order = Column(Integer)
    work_day = Column(DECIMAL(precision=8, scale=2))
    total_oil = Column(DECIMAL(precision=10, scale=2))
    average_oil = Column(DECIMAL(precision=6, scale=2))
    oil_gas_ratio = Column(DECIMAL(precision=5, scale=2))
    measure_cost = Column(DECIMAL(precision=10, scale=2))
    operating_cost = Column(DECIMAL(precision=10, scale=2))
    benefit_comparison = Column(DECIMAL(precision=10, scale=2))
    well_id = Column(Integer, ForeignKey('well_number.id'), nullable=False)

    wells = relationship("Well", back_populates="benefites")

    def __repr__(self):
        # 返回ORM映射数据模型
        return f"Benefit(id={self.id!r}, " \
               f"zq_order={self.zq_order!r}, " \
               f"work_day={self.work_day!r}), " \
               f"total_oil={self.total_oil!r}), " \
               f"average_oil={self.average_oil!r}, " \
               f"oil_gas_ratio={self.oil_gas_ratio!r}, " \
               f"measure_cost={self.measure_cost!r}, " \
               f"operating_cost={self.operting_cost!r}, " \
               f"benefit_comparison={self.benefit_comparison}"


# 首先在数据表里查重，如果DataFrame对象集合中的数据没有在数据表中则返回 True
def table_unique(Session, df_data):
    FIRST = df_data[0:1]
    LAST = df_data[len(df_data)-1:len(df_data)]
    pass


# 显示数据表里数据
def table_show(Session, df_data):
    pass


# 读取CSV,Excel文件，并向数据表里新增数据记录函数：table_add(df_data)
# df_data 是Pandas.DataFrame数据类型
def table_add(Session, df_data, oil_area):
    # create session and add objects
    # with Session(engine) as session:
    # Well , Benefit 表模板定义类—— model/Well.py, omdel/Benefit.py
    well_num = []
    well_date = [2006, 2009, 2010, 2011, 2012, 2013, 2015, 2016]
    with Session.begin() as session:
        for date, row in df_data.iterrows():
            # 为 Well,Benefit ORM 映射数据表赋值
            # 判断是否有效益
            if row["B"] > 0.0:
                info = '稠油井, 目前生产状态为正效益井'
            else:
                info = '稠油井, 目前生产状态为负效益井'

            # 新增数据
            u1 = Well(name=row["W"],
              oil_area=oil_area,
              birthday=datetime.date(random.choice(well_date), random.choice(range(1,12)), random.choice(range(1,30))),
              info=info,
              benefites=[
                  Benefit(zq_order=row["Z"],
                          work_day=row["D"],
                          total_oil=row["T"],
                          average_oil=row["A"],
                          oil_gas_ratio=row["G"],
                          measure_cost=row["M"],
                          operating_cost=row["O"],
                          benefit_comparison=row["B"]),
                  Benefit(zq_order=row["Z"]-1,
                          work_day=row["D1"],
                          total_oil=row["T1"],
                          average_oil=row["A1"],
                          oil_gas_ratio=row["G1"],
                          measure_cost=row["M1"],
                          operating_cost=row["O1"],
                          benefit_comparison=row["B1"])
              ])
            session.add(u1)
            well_num.append(row["W"])
    print(f'{well_num}')
    # session.commit()

# 程序运行入口：
if __name__ == "__main__":
    # 建立数据表连接
    engine = create_engine('sqlite:///snake_example.db', echo=True)

    # 创建数据表, 如果表已经存在则忽略此命令
    Base.metadata.create_all(engine)

    # 建立数据表工作手柄
    Session = sessionmaker(engine)
    oil_area = 'Shengke'

    # 数据查重
    if table_unique(Session, benefit_shk):
        # 调用数据表新增函数
        table_add(Session, benefit_shk, oil_area)
    else:
        table_show(Session, benefit_shk)


    print(f'--------------Shengke_Well Work End----------------')

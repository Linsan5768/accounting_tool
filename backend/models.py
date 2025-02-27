from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# 连接 SQLite 数据库（使用 accounting.db）
DATABASE_URL = "sqlite:///accounting.db"  
engine = create_engine(DATABASE_URL, echo=True)

# ORM 基类
Base = declarative_base()

# SQLAlchemy Session
Session = sessionmaker(bind=engine)

# 分类表
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    
    # 反向关系：一个分类对应多个记账记录
    records = relationship("Record", back_populates="category")

# 记账记录表
class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    remarks = Column(String)

    # 关联分类表
    category = relationship("Category", back_populates="records")

# 插入默认分类
def insert_default_categories(session):
    """初始化默认分类"""
    default_categories = ['餐饮', '话费', '理发', '交通', '洗衣', '超市购物', '零钱', '房租']
    
    existing_categories = {c.name for c in session.query(Category).all()}
    print("数据库已有类别:", existing_categories)  # 调试输出

    for name in default_categories:
        if name not in existing_categories:
            print(f"插入类别: {name}")  # 调试输出
            session.add(Category(name=name))
    
    session.commit()

# 创建表
def init_db():
    """初始化数据库"""
    Base.metadata.create_all(engine)
    with Session() as session:
        insert_default_categories(session)

# 运行数据库初始化
if __name__ == "__main__":
    init_db()
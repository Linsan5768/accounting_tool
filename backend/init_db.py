# backend/init_db.py
from models import engine, Base
# 运行这个脚本后，SQLite 数据库文件 accounting.db 应该会被创建
Base.metadata.create_all(engine)
print("数据库已初始化！")

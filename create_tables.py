from main import create_app
from app import db

# 创建应用实例
app = create_app()

# 在应用上下文中创建数据库表
with app.app_context():
    print("正在创建数据库表...")
    db.create_all()
    print("数据库表创建完成！")

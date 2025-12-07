from main import create_app
from app import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 直接创建所有表，确保新添加的表被创建
        db.create_all()
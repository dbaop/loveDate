from main import create_app
from app import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 导入所有模型，确保它们被注册到SQLAlchemy
        from app.models.user import User
        from app.models.therapist import Therapist
        from app.models.service import Service
        from app.models.order import Order
        from app.models.feedback import Feedback
        from app.models.message import Message
        
        # 直接创建所有表，确保新添加的表和字段被创建
        db.create_all()
        print("数据库表创建/更新完成")
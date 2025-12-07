from main import create_app
from app import db
from app.models.user import User
import hashlib

app = create_app()

with app.app_context():
    # 检查是否已存在管理员用户
    admin = User.query.filter_by(phone='13800138888').first()
    if admin:
        print('管理员用户已存在')
    else:
        # 创建管理员用户
        admin = User(
            username='admin',
            phone='13800138888',
            password_hash=hashlib.sha256('admin123'.encode()).hexdigest(),  # 使用SHA256加密密码
            role='admin',
            status=1
        )
        db.session.add(admin)
        db.session.commit()
        print('管理员用户创建成功')

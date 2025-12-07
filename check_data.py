from main import create_app
from app import db
from app.models.user import User
from app.models.therapist import Therapist

app = create_app()
with app.app_context():
    # 检查用户表
    all_users = User.query.all()
    print("现有用户总数:", len(all_users))
    
    # 显示用户信息
    for user in all_users:
        print(f"用户ID: {user.id}, 用户名: {user.username}, 手机号: {user.phone}")
    
    # 检查治疗师表
    all_therapists = Therapist.query.all()
    print("\n现有治疗师总数:", len(all_therapists))
    
    # 显示治疗师信息
    for therapist in all_therapists:
        print(f"治疗师ID: {therapist.id}, 姓名: {therapist.name}, 状态: {therapist.status}, 手机号: {therapist.phone}")

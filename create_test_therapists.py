from main import create_app, db
from app.models.therapist import Therapist
from app.models.user import User
from app.models.service import Service

def create_test_therapists():
    app = create_app()
    with app.app_context():
        # 创建一些测试理疗师用户
        therapists = [
            {
                'name': '张医生',
                'phone': '13900139001',
                'id_card': '110101199001011234',
                'age': 35,
                'certification': '高级理疗师证书',
                'experience_years': 10,
                'specialty': '中医推拿',
                'rating': 4.8,
                'service_count': 120,
                'status': 1,
                'avatar': 'https://example.com/avatar1.jpg',
                'introduction': '10年中医推拿经验，擅长缓解颈椎、腰椎疼痛，使用传统中医手法结合现代理疗技术。'
            },
            {
                'name': '李按摩师',
                'phone': '13900139002',
                'id_card': '110101199202022345',
                'age': 32,
                'certification': '中级理疗师证书',
                'experience_years': 7,
                'specialty': '精油按摩',
                'rating': 4.6,
                'service_count': 95,
                'status': 1,
                'avatar': 'https://example.com/avatar2.jpg',
                'introduction': '专业精油按摩师，擅长全身精油SPA，帮助客户放松身心，改善睡眠质量。'
            },
            {
                'name': '王理疗师',
                'phone': '13900139003',
                'id_card': '110101199503033456',
                'age': 28,
                'certification': '初级理疗师证书',
                'experience_years': 3,
                'specialty': '拔罐刮痧',
                'rating': 4.5,
                'service_count': 60,
                'status': 1,
                'avatar': 'https://example.com/avatar3.jpg',
                'introduction': '擅长传统拔罐刮痧疗法，能够有效缓解身体疲劳和不适症状。'
            }
        ]
        
        created_count = 0
        for therapist_data in therapists:
            # 检查手机号是否已存在
            existing_user = User.query.filter_by(phone=therapist_data['phone']).first()
            if not existing_user:
                # 创建用户
                user = User(
                    username=therapist_data['name'],
                    phone=therapist_data['phone'],
                    password_hash='123456',
                    role='therapist'
                )
                db.session.add(user)
                db.session.flush()  # 获取用户ID
                
                # 创建理疗师信息
                therapist = Therapist(
                    id=user.id,  # 使用用户ID作为理疗师ID
                    name=therapist_data['name'],
                    phone=therapist_data['phone'],
                    id_card=therapist_data['id_card'],
                    age=therapist_data['age'],
                    certification=therapist_data['certification'],
                    experience_years=therapist_data['experience_years'],
                    specialty=therapist_data['specialty'],
                    rating=therapist_data['rating'],
                    service_count=therapist_data['service_count'],
                    status=therapist_data['status'],
                    avatar=therapist_data['avatar'],
                    introduction=therapist_data['introduction']
                )
                
                # 关联所有服务项目
                all_services = Service.query.all()
                therapist.service_items = all_services
                
                db.session.add(therapist)
                created_count += 1
            else:
                print(f'Therapist with phone {therapist_data["phone"]} already exists')
        
        db.session.commit()
        print(f'Successfully created {created_count} test therapists')

if __name__ == '__main__':
    create_test_therapists()
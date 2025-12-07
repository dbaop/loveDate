from main import create_app
from app import db
from app.models.therapist import ServiceItem

app = create_app()
with app.app_context():
    # 检查是否已有服务项目
    existing_services = ServiceItem.query.count()
    
    if existing_services == 0:
        # 添加默认服务套餐
        default_services = [
            {
                'name': '经典全身按摩',
                'description': '90分钟全身精油按摩，缓解疲劳，放松身心',
                'duration': 90,
                'price': 198.0,
                'category': 'classic'
            },
            {
                'name': '豪华SPA套餐',
                'description': '120分钟豪华SPA体验，包括精油按摩、热石疗法和面部护理',
                'duration': 120,
                'price': 298.0,
                'category': 'special'
            },
            {
                'name': '局部深度按摩',
                'description': '60分钟肩颈或腰部深度按摩，缓解肌肉紧张',
                'duration': 60,
                'price': 128.0,
                'category': 'classic'
            },
            {
                'name': '精油背部按摩套餐',
                'description': '75分钟背部精油按摩，促进血液循环，缓解压力',
                'duration': 75,
                'price': 168.0,
                'category': 'special'
            }
        ]
        
        # 插入默认服务项目
        for service_data in default_services:
            service = ServiceItem(**service_data)
            db.session.add(service)
        
        db.session.commit()
        print(f"成功添加 {len(default_services)} 个默认服务套餐")
    else:
        print(f"数据库中已有 {existing_services} 个服务项目，跳过初始化")
        
        # 显示现有服务项目
        existing = ServiceItem.query.all()
        for service in existing:
            print(f"- {service.name}: ￥{service.price} ({service.duration}分钟)")

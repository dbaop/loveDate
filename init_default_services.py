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
                'name': 'Classic Full Body Massage',
                'description': '90 minutes full body oil massage, relieve fatigue and relax body and mind',
                'duration': 90,
                'price': 198.0,
                'category': 'classic'
            },
            {
                'name': 'Premium SPA Package',
                'description': '120 minutes luxury SPA experience, including oil massage, hot stone therapy and facial care',
                'duration': 120,
                'price': 298.0,
                'category': 'special'
            },
            {
                'name': 'Local Deep Massage',
                'description': '60 minutes deep massage for shoulder/neck or waist, relieve muscle tension',
                'duration': 60,
                'price': 128.0,
                'category': 'classic'
            },
            {
                'name': 'Oil Back Massage Package',
                'description': '75 minutes back oil massage, promote blood circulation and relieve pressure',
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

from main import create_app
from app.models.therapist import Therapist, ServiceItem

# 创建应用实例
app = create_app()

with app.app_context():
    # 查询技师列表
    therapists = Therapist.query.all()
    print("技师列表:")
    for t in therapists:
        print(f"ID: {t.id}, 姓名: {t.name}, 状态: {t.status}")
    
    # 查询服务项目列表
    service_items = ServiceItem.query.all()
    print("\n服务项目:")
    for s in service_items:
        print(f"ID: {s.id}, 名称: {s.name}, 状态: {s.status}")
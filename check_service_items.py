from main import create_app, db
from app.models.therapist import ServiceItem

def check_service_items():
    app = create_app()
    with app.app_context():
        # 获取所有ServiceItem
        service_items = ServiceItem.query.all()
        if service_items:
            print(f"找到 {len(service_items)} 个ServiceItem:")
            for item in service_items:
                print(f"- ID: {item.id}, 名称: {item.name}, 价格: {item.price}, 时长: {item.duration}分钟")
        else:
            print("没有找到任何ServiceItem数据")

if __name__ == '__main__':
    check_service_items()
from main import create_app, db
from app.models.therapist import Therapist, ServiceItem

def associate_services_to_therapists():
    app = create_app()
    with app.app_context():
        # 获取所有服务项目
        all_services = ServiceItem.query.all()
        if not all_services:
            print("没有找到服务项目，请先初始化服务数据")
            return
        
        # 获取所有治疗师
        therapists = Therapist.query.all()
        if not therapists:
            print("没有找到治疗师，请先创建治疗师数据")
            return
        
        # 为每个治疗师关联所有服务项目
        for therapist in therapists:
            therapist.service_items = all_services
            print(f"为治疗师 {therapist.name} (ID: {therapist.id}) 关联了 {len(all_services)} 个服务项目")
        
        db.session.commit()
        print("\n成功为所有治疗师关联服务项目")

if __name__ == '__main__':
    associate_services_to_therapists()
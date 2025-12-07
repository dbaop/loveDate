from main import create_app
from app.models.therapist import Therapist

app = create_app()
with app.app_context():
    # 查询所有技师，不按状态过滤
    therapists = Therapist.query.all()
    print("所有技师列表:")
    for t in therapists:
        print(f"ID: {t.id}, 姓名: {t.name}, 状态: {t.status}, 手机号: {t.phone}")
    
    # 特别查询ID为1的技师
    therapist_id_1 = Therapist.query.get(1)
    print(f"\nID为1的技师信息: {therapist_id_1}")
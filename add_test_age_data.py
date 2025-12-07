from main import create_app, db
from app.models.therapist import Therapist

def add_test_age_data():
    app = create_app()
    with app.app_context():
        # 为所有理疗师设置随机年龄（25-45岁）
        therapists = Therapist.query.all()
        import random
        
        for therapist in therapists:
            # 如果年龄为空，设置一个随机年龄
            if therapist.age is None:
                therapist.age = random.randint(25, 45)
                db.session.add(therapist)
        
        db.session.commit()
        print(f'Successfully updated age for {len(therapists)} therapists')

if __name__ == '__main__':
    add_test_age_data()
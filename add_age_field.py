from main import create_app, db
from app.models.therapist import Therapist

def add_age_field():
    app = create_app()
    with app.app_context():
        # 检查age字段是否已经存在
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('therapists')
        column_names = [col['name'] for col in columns]
        
        if 'age' not in column_names:
            # 使用SQLAlchemy的连接来执行SQL语句
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE therapists ADD age INTEGER'))
                conn.commit()
            print('Successfully added age field to therapists table')
        else:
            print('Age field already exists')

if __name__ == '__main__':
    add_age_field()
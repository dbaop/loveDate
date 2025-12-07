from main import create_app
from app.models.therapist import Therapist, ServiceItem
from app import db

# 创建应用实例
app = create_app()

with app.app_context():
    # 获取数据库连接
    conn = db.engine.connect()
    
    try:
        # 查询therapists表的结构
        result = conn.execute(db.text("PRAGMA table_info(therapists)"))
        
        print("Therapists table structure:")
        print("=" * 60)
        print(f"{'Column ID':<10} {'Column Name':<30} {'Data Type':<15} {'NotNull':<5} {'Default':<10}")
        print("=" * 60)
        
        for row in result:
            # 处理可能的None值
            col_id = row[0] or ""
            col_name = row[1] or ""
            data_type = row[2] or ""
            not_null = row[3] or ""
            default_val = row[4] or ""
            print(f"{col_id:<10} {col_name:<30} {data_type:<15} {not_null:<5} {default_val:<10}")
            
        print("\n\nChecking for new fields:")
        new_fields = ['gender', 'id_card_front', 'id_card_back', 'id_card_handheld']
        
        # 查询表中的所有字段
        fields_result = conn.execute(db.text("PRAGMA table_info(therapists)"))
        existing_fields = [row[1] for row in fields_result]
        
        for field in new_fields:
            if field in existing_fields:
                print(f"✓ Field '{field}' exists in therapists table")
            else:
                print(f"✗ Field '{field}' DOES NOT exist in therapists table")
                
        # 查询技师列表
        print("\n\nTherapists list:")
        print("=" * 60)
        therapists = Therapist.query.all()
        if therapists:
            for t in therapists:
                print(f"ID: {t.id}, 姓名: {t.name}, 状态: {t.status}")
        else:
            print("No therapists found")
            
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        conn.close()
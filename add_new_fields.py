from main import create_app
from app import db

# 创建应用实例
app = create_app()

with app.app_context():
    # 获取数据库连接
    conn = db.engine.connect()
    
    try:
        # 添加gender字段
        conn.execute(db.text("ALTER TABLE therapists ADD COLUMN gender INTEGER"))
        print("✓ Added gender field")
        
        # 添加id_card_front字段
        conn.execute(db.text("ALTER TABLE therapists ADD COLUMN id_card_front VARCHAR(255)"))
        print("✓ Added id_card_front field")
        
        # 添加id_card_back字段
        conn.execute(db.text("ALTER TABLE therapists ADD COLUMN id_card_back VARCHAR(255)"))
        print("✓ Added id_card_back field")
        
        # 添加id_card_handheld字段
        conn.execute(db.text("ALTER TABLE therapists ADD COLUMN id_card_handheld VARCHAR(255)"))
        print("✓ Added id_card_handheld field")
        
        print("\n✅ All new fields have been successfully added to the therapists table!")
        
    except Exception as e:
        print(f"\n❌ Error adding fields: {e}")
    finally:
        conn.close()

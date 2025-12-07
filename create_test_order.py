import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_app, db
from app.models.user import User
from app.models.therapist import Therapist
from app.models.order import Order
from app.models.service import Service

# 创建应用
app = create_app()

with app.app_context():
    try:
        # 检查是否已有订单数据
        existing_orders = Order.query.count()
        if existing_orders > 0:
            print(f"数据库中已有 {existing_orders} 个订单，跳过创建测试数据")
            sys.exit(0)

        # 获取测试用户（假设已有用户）
        test_user = User.query.first()
        if not test_user:
            print("数据库中没有用户，无法创建订单")
            sys.exit(1)

        # 获取测试理疗师（假设已有理疗师）
        test_therapist = Therapist.query.first()
        if not test_therapist:
            print("数据库中没有理疗师，无法创建订单")
            sys.exit(1)

        # 获取测试服务（假设已有服务）
        test_service = Service.query.first()
        if not test_service:
            # 创建一个测试服务
            test_service = Service(
                name="全身按摩",
                description="60分钟全身放松按摩",
                duration=60,
                price=298,
                category="massage",
                is_active=True
            )
            db.session.add(test_service)
            db.session.commit()

        # 创建测试订单
        import uuid
        
        test_order = Order(
            order_no=f"ORD-{uuid.uuid4().hex[:12].upper()}",
            user_id=test_user.id,
            therapist_id=test_therapist.id,
            service_item_id=test_service.id,
            service_name=test_service.name,
            duration=test_service.duration,
            price=float(test_service.price),
            service_time=datetime.now() - timedelta(days=1),
            status=4,  # 已完成状态
            service_address="北京市朝阳区测试地址",
            contact_phone=test_user.phone,
            payment_status=1,  # 已支付
            payment_method="wechat",
            paid_at=datetime.now() - timedelta(days=1)
        )
        db.session.add(test_order)
        db.session.commit()

        print(f"成功创建测试订单: ID={test_order.id}, 订单号={test_order.order_no}")
        print("可使用此订单ID测试评价提交功能")

    except Exception as e:
        print(f"创建测试订单时出错: {e}")
        db.session.rollback()
        sys.exit(1)
    finally:
        db.session.close()

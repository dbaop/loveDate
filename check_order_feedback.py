from main import create_app
from app import db
from app.models.order import Order
from app.models.feedback import Feedback

app = create_app()

with app.app_context():
    # 查询所有已完成的订单和它们的评价情况
    completed_orders = Order.query.filter_by(status=4).all()
    
    print("已完成订单的评价情况：")
    print("订单ID | 订单号 | 评价状态")
    print("---------------------------")
    
    for order in completed_orders:
        has_feedback = "已评价" if order.feedback else "未评价"
        print(f"{order.id} | {order.order_no} | {has_feedback}")
    
    # 查询订单ID为1的详细信息
    specific_order_id = 1
    specific_order = Order.query.get(specific_order_id)
    if specific_order:
        print(f"\n订单ID {specific_order_id}的详细信息：")
        print(f"订单号：{specific_order.order_no}")
        print(f"订单状态：{specific_order.status} (4表示已完成)")
        print(f"评价状态：{'已评价' if specific_order.feedback else '未评价'}")
        if specific_order.feedback:
            print(f"评价内容：{specific_order.feedback.content}")
            print(f"评分：{specific_order.feedback.rating}")
            print(f"评价标签：{specific_order.feedback.tags}")
            print(f"评价时间：{specific_order.feedback.created_at}")
    else:
        print(f"未找到订单ID {specific_order_id}")

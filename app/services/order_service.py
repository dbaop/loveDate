from app.models.order import Order, OrderStatus, PaymentStatus, PaymentMethod
from app.models.user import User
from app.models.therapist import Therapist, ServiceItem
from app import db
import random
import string
import datetime
import json


class OrderService:
    @staticmethod
    def create_order(user_id, data):
        """创建订单"""
        # 验证技师和服务项目
        therapist = Therapist.query.filter_by(id=data['therapist_id'], status=1).first()
        if not therapist:
            raise Exception("技师不可用")

        # 获取服务项目信息（创建快照）
        service_item = ServiceItem.query.filter_by(id=data['service_item_id'], status=1).first()
        if not service_item:
            raise Exception("服务项目不可用")

        # 转换服务时间为datetime对象
        service_time = datetime.datetime.fromisoformat(data['service_time'])
        
        # 创建订单
        order = Order(
            order_no=OrderService._generate_order_no(),
            user_id=user_id,
            therapist_id=data['therapist_id'],
            service_item_id=data['service_item_id'],
            service_name=service_item.name,
            duration=service_item.duration,
            price=service_item.price,
            service_time=service_time,
            service_address=data['service_address'],
            contact_phone=data['contact_phone'],
            remark=data.get('remark')
        )

        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def get_user_orders(user_id, page, size, status=None):
        """获取用户订单列表"""
        query = Order.query.filter_by(user_id=user_id)

        if status is not None:
            query = query.filter_by(status=status)

        # 按创建时间倒序排列
        query = query.order_by(Order.created_at.desc())

        # 分页
        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'size': size
        }

    @staticmethod
    def get_order_detail(user_id, order_id):
        """获取订单详情"""
        return Order.query.filter_by(id=order_id, user_id=user_id).first()

    @staticmethod
    def cancel_order(user_id, order_id):
        """取消订单"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise Exception("订单不存在")

        # 检查订单状态是否可以取消
        if order.status > OrderStatus.ON_THE_WAY:
            raise Exception("订单无法取消")

        order.status = OrderStatus.CANCELLED
        db.session.commit()

    # 技师端订单管理功能
    @staticmethod
    def get_therapist_orders(therapist_id, page, size, status=None):
        """获取技师订单列表"""
        query = Order.query.filter_by(therapist_id=therapist_id)

        if status is not None:
            query = query.filter_by(status=status)

        # 按创建时间倒序排列
        query = query.order_by(Order.created_at.desc())

        # 分页
        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'size': size
        }

    @staticmethod
    def accept_order(therapist_id, order_id):
        """技师接受订单"""
        order = Order.query.filter_by(id=order_id, therapist_id=therapist_id, status=OrderStatus.PENDING).first()
        if not order:
            raise Exception("订单不存在或状态不允许")

        order.status = OrderStatus.ACCEPTED
        db.session.commit()
        return order

    @staticmethod
    def start_journey(therapist_id, order_id):
        """技师出发"""
        order = Order.query.filter_by(id=order_id, therapist_id=therapist_id, status=OrderStatus.ACCEPTED).first()
        if not order:
            raise Exception("订单不存在或状态不允许")

        order.status = OrderStatus.ON_THE_WAY
        db.session.commit()
        return order

    @staticmethod
    def start_service(therapist_id, order_id):
        """开始服务"""
        order = Order.query.filter_by(id=order_id, therapist_id=therapist_id, status=OrderStatus.ON_THE_WAY).first()
        if not order:
            raise Exception("订单不存在或状态不允许")

        order.status = OrderStatus.IN_SERVICE
        db.session.commit()
        return order

    @staticmethod
    def complete_order(therapist_id, order_id):
        """完成服务"""
        order = Order.query.filter_by(id=order_id, therapist_id=therapist_id, status=OrderStatus.IN_SERVICE).first()
        if not order:
            raise Exception("订单不存在或状态不允许")

        order.status = OrderStatus.COMPLETED
        
        # 更新技师的服务次数
        therapist = Therapist.query.get(therapist_id)
        if therapist:
            therapist.service_count += 1
        
        db.session.commit()
        return order

    @staticmethod
    def _generate_order_no():
        """生成订单号"""
        prefix = "ORD"
        timestamp = str(int(datetime.datetime.now().timestamp()))
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{prefix}{timestamp}{random_str}"

    @staticmethod
    def create_payment(order_id, user_id, payment_method):
        """创建支付"""
        # 验证订单
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise Exception("订单不存在")

        if order.status == OrderStatus.CANCELLED:
            raise Exception("订单已取消")

        if order.payment_status == PaymentStatus.PAID:
            raise Exception("订单已支付")

        # 模拟支付调用，实际应调用微信/支付宝SDK
        # 这里生成一个模拟的支付参数
        payment_params = {
            'order_no': order.order_no,
            'amount': order.price,
            'payment_method': payment_method,
            'subject': f"预约服务: {order.service_name}",
            'timestamp': int(datetime.datetime.now().timestamp()),
            'nonce_str': ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
            # 实际应用中这里应该包含签名、支付跳转链接等
        }

        return {
            'order_id': order.id,
            'payment_params': payment_params,
            'order_info': {
                'order_no': order.order_no,
                'amount': order.price,
                'service_name': order.service_name,
                'service_time': order.service_time.isoformat() if order.service_time else None
            }
        }

    @staticmethod
    def payment_callback(data):
        """支付回调处理"""
        # 解析支付回调数据
        # 实际应用中需要验证签名和支付平台的真实性
        order_no = data.get('order_no')
        transaction_id = data.get('transaction_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')
        status = data.get('status')

        if not all([order_no, transaction_id, payment_method, amount, status]):
            raise Exception("回调参数不完整")

        # 查找订单
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            raise Exception("订单不存在")

        # 更新支付状态
        if status == 'success':
            order.payment_status = PaymentStatus.PAID
            order.payment_method = payment_method
            order.transaction_id = transaction_id
            order.paid_at = datetime.datetime.now()
            # 支付成功后可以触发其他业务逻辑，如通知技师
        else:
            order.payment_status = PaymentStatus.PAY_FAILED

        db.session.commit()
        return order

    @staticmethod
    def get_payment_status(order_id, user_id):
        """查询支付状态"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise Exception("订单不存在")

        return {
            'order_no': order.order_no,
            'payment_status': order.payment_status,
            'payment_method': order.payment_method,
            'paid_at': order.paid_at.isoformat() if order.paid_at else None,
            'transaction_id': order.transaction_id
        }

    @staticmethod
    def refund(order_id, user_id, amount, reason):
        """申请退款"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            raise Exception("订单不存在")

        if order.payment_status != PaymentStatus.PAID:
            raise Exception("订单未支付，无法退款")

        # 验证退款金额
        if amount > order.price:
            raise Exception("退款金额不能超过订单金额")

        # 模拟退款调用，实际应调用微信/支付宝SDK
        # 这里生成一个模拟的退款结果
        refund_result = {
            'refund_no': f"REF{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}",
            'amount': amount,
            'status': 'success',
            'transaction_id': order.transaction_id
        }

        # 更新订单支付状态为已退款
        order.payment_status = PaymentStatus.REFUNDED
        db.session.commit()

        return refund_result

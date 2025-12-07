from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_no = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    therapist_id = Column(Integer, ForeignKey('therapists.id'))
    service_item_id = Column(Integer)  # 服务项目ID
    service_name = Column(String(100))  # 服务名称(快照)
    duration = Column(Integer)  # 时长(分钟)
    price = Column(Float)  # 价格
    service_time = Column(DateTime)  # 服务时间
    service_address = Column(Text)  # 服务地址
    contact_phone = Column(String(20))  # 联系电话
    status = Column(Integer, default=0)  # 0:待接单, 1:已接单, 2:技师出发, 3:服务中, 4:已完成, 5:已取消
    remark = Column(Text)  # 备注
    # 支付相关字段
    payment_status = Column(Integer, default=0)  # 0:未支付, 1:已支付, 2:支付失败, 3:已退款
    payment_method = Column(String(20))  # 支付方式: wechat, alipay, etc.
    transaction_id = Column(String(100))  # 支付平台交易ID
    paid_at = Column(DateTime)  # 支付时间
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="orders")
    therapist = relationship("Therapist", back_populates="orders")
    feedback = relationship("Feedback", back_populates="order", uselist=False)


class OrderStatus:
    PENDING = 0  # 待接单
    ACCEPTED = 1  # 已接单
    ON_THE_WAY = 2  # 技师出发
    IN_SERVICE = 3  # 服务中
    COMPLETED = 4  # 已完成
    CANCELLED = 5  # 已取消


class PaymentStatus:
    UNPAID = 0  # 未支付
    PAID = 1  # 已支付
    PAY_FAILED = 2  # 支付失败
    REFUNDED = 3  # 已退款


class PaymentMethod:
    WECHAT = 'wechat'  # 微信支付
    ALIPAY = 'alipay'  # 支付宝
    CASH = 'cash'  # 现金支付

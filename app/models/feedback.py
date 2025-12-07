from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app import db


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True, nullable=False)  # 一个订单只能评价一次
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    therapist_id = Column(Integer, ForeignKey('therapists.id'), nullable=False)
    rating = Column(Float, nullable=False)  # 评分，1-5分
    content = Column(Text)  # 评价内容
    tags = Column(String(200))  # 评价标签，用逗号分隔
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="feedbacks")
    therapist = relationship("Therapist", back_populates="feedbacks")
    order = relationship("Order", back_populates="feedback")


# 也可以在用户和技师模型中添加反向关系
# 在User模型中添加：feedbacks = relationship("Feedback", back_populates="user")
# 在Therapist模型中添加：feedbacks = relationship("Feedback", back_populates="therapist")
# 在Order模型中添加：feedback = relationship("Feedback", back_populates="order", uselist=False)
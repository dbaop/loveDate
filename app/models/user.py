from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    password_hash = Column(String(100))  # 密码哈希
    avatar = Column(String(255))
    status = Column(Integer, default=1)  # 1:正常, 0:禁用
    role = Column(String(20), default='user')  # user:普通用户, therapist:治疗师, admin:管理员
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 关系
    orders = relationship("Order", back_populates="user")
    addresses = relationship("UserAddress", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class UserAddress(db.Model):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'))
    name = Column(String(50))  # 地址名称
    address = Column(Text, nullable=False)  # 详细地址
    latitude = Column(String(20))  # 纬度
    longitude = Column(String(20))  # 经度
    is_default = Column(Integer, default=0)  # 是否默认地址
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="addresses")

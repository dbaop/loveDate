from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
import datetime
from app import db


class Therapist(db.Model):
    __tablename__ = 'therapists'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    id_card = Column(String(20))  # 身份证号
    age = Column(Integer)  # 年龄
    certification = Column(String(255))  # 资格证书
    experience_years = Column(Integer)  # 经验年限
    specialty = Column(String(255))  # 专长
    rating = Column(Float, default=5.0)  # 评分
    service_count = Column(Integer, default=0)  # 服务次数
    status = Column(Integer, default=0)  # 0:待审核, 1:正常, 2:暂停
    avatar = Column(String(255))  # 头像
    introduction = Column(Text)  # 简介
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 关联服务项目
    service_items = relationship("ServiceItem", secondary="therapist_services")
    orders = relationship("Order", back_populates="therapist")
    feedbacks = relationship("Feedback", back_populates="therapist")


class ServiceItem(db.Model):
    __tablename__ = 'service_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration = Column(Integer)  # 时长(分钟)
    price = Column(Float, nullable=False)  # 价格
    category = Column(String(50))  # 分类: classic, special, custom
    status = Column(Integer, default=1)  # 1:启用, 0:禁用
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# 技师与服务项目的关联表
therapist_services = db.Table('therapist_services',
                              Column('therapist_id', Integer, db.ForeignKey('therapists.id')),
                              Column('service_item_id', Integer, db.ForeignKey('service_items.id'))
                              )

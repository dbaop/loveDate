from app import db
from datetime import datetime


class Service(db.Model):
    """服务项目模型"""
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='服务名称')
    description = db.Column(db.Text, nullable=False, comment='服务描述')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='服务价格')
    duration = db.Column(db.Integer, nullable=False, comment='服务时长(分钟)')
    category = db.Column(db.String(50), nullable=False, comment='服务分类')
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    
    # 关系 - 暂时注释掉，因为Order模型中没有对应的service字段
    # orders = db.relationship('Order', back_populates='service')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'duration': self.duration,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

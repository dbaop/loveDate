from app import db
from datetime import datetime


class Message(db.Model):
    """消息模型"""
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, nullable=False, comment='发送者ID')
    sender_role = db.Column(db.String(20), nullable=False, comment='发送者角色: user或therapist')
    receiver_id = db.Column(db.Integer, nullable=False, comment='接收者ID')
    receiver_role = db.Column(db.String(20), nullable=False, comment='接收者角色: user或therapist')
    order_id = db.Column(db.Integer, nullable=False, comment='关联的订单ID')
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    is_read = db.Column(db.Boolean, default=False, nullable=False, comment='是否已读')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_role': self.sender_role,
            'receiver_id': self.receiver_id,
            'receiver_role': self.receiver_role,
            'order_id': self.order_id,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

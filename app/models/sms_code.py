from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app import db

class SMSCode(db.Model):
    __tablename__ = 'sms_codes'

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    status = Column(Integer, default=0)  # 0:未使用, 1:已使用, 2:已过期
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self):
        """检查验证码是否过期"""
        return datetime.datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f'<SMSCode {self.phone}: {self.code}>'
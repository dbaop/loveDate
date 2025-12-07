import random
import datetime
from app import db
from app.models.sms_code import SMSCode
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMSService:
    @staticmethod
    def generate_code(phone):
        """生成并保存短信验证码"""
        # 生成6位随机验证码
        code = ''.join(random.choices('0123456789', k=6))
        
        # 设置验证码有效期为10分钟
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        
        # 检查是否已存在未使用的验证码，如果有则更新
        existing_code = SMSCode.query.filter_by(phone=phone, status=0).first()
        if existing_code:
            existing_code.code = code
            existing_code.expires_at = expires_at
        else:
            # 创建新的验证码记录
            sms_code = SMSCode(
                phone=phone,
                code=code,
                expires_at=expires_at
            )
            db.session.add(sms_code)
        
        db.session.commit()
        
        # 这里应该调用短信发送API，目前仅记录日志
        logger.info(f"向{phone}发送验证码: {code}")
        
        return code
    
    @staticmethod
    def verify_code(phone, code):
        """验证短信验证码"""
        if not phone or not code:
            raise Exception("手机号和验证码不能为空")
        
        # 查找最新的未使用验证码
        sms_code = SMSCode.query.filter_by(phone=phone, status=0).order_by(SMSCode.created_at.desc()).first()
        
        if not sms_code:
            raise Exception("验证码不存在或已使用")
        
        # 检查验证码是否过期
        if sms_code.is_expired():
            sms_code.status = 2  # 标记为已过期
            db.session.commit()
            raise Exception("验证码已过期")
        
        # 检查验证码是否正确
        if sms_code.code != code:
            raise Exception("验证码错误")
        
        # 标记验证码为已使用
        sms_code.status = 1
        db.session.commit()
        
        return True
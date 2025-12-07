from app.models.user import User, UserAddress
from app import db
from app.utils.auth import generate_token
from app.services.sms_service import SMSService
import hashlib


class UserService:
    @staticmethod
    def register(data):
        """用户注册"""
        try:
            import logging
            logger = logging.getLogger('user_service')
            
            logger.info(f"Register request received with data: {data}")
            
            # 验证必要参数
            if 'phone' not in data:
                logger.error("缺少必要参数: phone")
                raise ValueError("缺少必要参数: phone")
            if 'username' not in data:
                logger.error("缺少必要参数: username")
                raise ValueError("缺少必要参数: username")
                
            phone = data['phone']
            username = data['username']
            role = data.get('role', 'user')
            
            logger.info(f"Phone: {phone}, Username: {username}, Role: {role}")
            
            # 检查手机号是否已存在
            existing_user = User.query.filter_by(phone=phone).first()
            if existing_user:
                logger.error(f"手机号已注册: {phone}")
                raise ValueError("手机号已注册")

            # 创建用户
            user = User(
                username=username,
                phone=phone,
                role=role
            )

            # 如果提供了密码，则进行加密存储
            if 'password' in data:
                user.password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
                logger.info("密码已加密存储")

            db.session.add(user)
            db.session.commit()
            logger.info(f"用户注册成功: {user.id}")
            return user
        except Exception as e:
            logger.error(f"注册失败: {str(e)}", exc_info=True)
            db.session.rollback()
            raise e

    @staticmethod
    def login(data):
        """用户登录"""
        # 验证必要参数
        if 'phone' not in data:
            raise Exception("缺少必要参数: phone")
        
        # 尝试同时使用手机号或用户名登录
        username_or_phone = data['phone']
        user = User.query.filter((User.phone == username_or_phone) | (User.username == username_or_phone)).first()
        if not user:
            raise Exception("用户不存在")

        # 验证密码
        if 'password' in data and hasattr(user, 'password_hash'):
            password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
            if user.password_hash != password_hash:
                raise Exception("密码错误")

        # 生成token
        token = generate_token(user.id)
        return token

    @staticmethod
    def login_with_sms(data):
        """通过短信验证码登录"""
        # 验证必要参数
        if 'phone' not in data or 'code' not in data:
            raise Exception("缺少必要参数: phone或code")
        
        phone = data['phone']
        code = data['code']
        
        # 验证短信验证码
        SMSService.verify_code(phone, code)
        
        # 检查用户是否存在，如果不存在则自动注册
        user = User.query.filter_by(phone=phone).first()
        if not user:
            # 自动注册用户
            username = phone[-8:]  # 使用手机号后8位作为用户名
            user = User(
                username=username,
                phone=phone,
                role='user'
            )
            db.session.add(user)
            db.session.commit()
        
        # 生成token
        token = generate_token(user.id)
        return token

    @staticmethod
    def get_user_addresses(user_id):
        """获取用户地址列表"""
        return UserAddress.query.filter_by(user_id=user_id).all()

    @staticmethod
    def add_user_address(user_id, data):
        """添加用户地址"""
        # 检查是否需要设置为默认地址
        is_default = data.get('is_default', 0)
        if is_default:
            # 将其他地址设为非默认
            UserAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})

        address = UserAddress(
            user_id=user_id,
            name=data.get('name'),
            address=data['address'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            is_default=is_default
        )

        db.session.add(address)
        db.session.commit()
        return address

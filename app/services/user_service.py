from app.models.user import User, UserAddress
from app import db
from app.utils.auth import generate_token
import hashlib


class UserService:
    @staticmethod
    def register(data):
        """用户注册"""
        # 验证必要参数
        if 'phone' not in data:
            raise Exception("缺少必要参数: phone")
        if 'username' not in data:
            raise Exception("缺少必要参数: username")
            
        # 检查手机号是否已存在
        existing_user = User.query.filter_by(phone=data['phone']).first()
        if existing_user:
            raise Exception("手机号已注册")

        # 创建用户
        user = User(
            username=data['username'],
            phone=data['phone'],
            role=data.get('role', 'user')  # 保存角色，默认普通用户
        )

        # 如果提供了密码，则进行加密存储
        if 'password' in data:
            user.password_hash = hashlib.sha256(data['password'].encode()).hexdigest()

        db.session.add(user)
        db.session.commit()
        return user

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

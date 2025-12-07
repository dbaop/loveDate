import requests
import logging
from app import db
from app.models.user import User
from app.utils.auth import generate_token

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WechatService:
    # 微信开发平台参数，实际部署时应从配置文件读取
    APP_ID = 'your_wechat_app_id'  # 微信小程序AppID
    APP_SECRET = 'your_wechat_app_secret'  # 微信小程序AppSecret
    
    @staticmethod
    def login_with_wechat(code):
        """
        通过微信小程序code登录
        :param code: 微信登录获取的code
        :return: 本地生成的token
        """
        try:
            # 1. 用code换取openid和session_key
            wechat_response = WechatService._get_wechat_openid(code)
            if 'errcode' in wechat_response:
                logger.error(f"微信API错误: {wechat_response}")
                raise Exception(f"微信登录失败: {wechat_response.get('errmsg', '未知错误')}")
            
            openid = wechat_response.get('openid')
            unionid = wechat_response.get('unionid')
            
            if not openid:
                raise Exception("获取微信openid失败")
            
            # 2. 根据openid查找或创建用户
            user = User.query.filter_by(wx_openid=openid).first()
            
            if not user:
                # 如果有手机号，尝试通过手机号关联用户
                # 这里可以扩展为让用户先绑定手机号
                user = User(
                    username=f'wx_{openid[:8]}',
                    phone='',  # 微信登录初始无手机号
                    wx_openid=openid,
                    wx_unionid=unionid
                )
                db.session.add(user)
                db.session.commit()
            
            # 3. 生成token
            token = generate_token(user.id)
            return token, user
            
        except requests.RequestException as e:
            logger.error(f"微信API请求失败: {str(e)}")
            raise Exception("微信登录请求失败")
        except Exception as e:
            logger.error(f"微信登录处理失败: {str(e)}")
            raise
    
    @staticmethod
    def _get_wechat_openid(code):
        """
        调用微信API获取openid和session_key
        :param code: 微信登录获取的code
        :return: 微信API返回的结果
        """
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': WechatService.APP_ID,
            'secret': WechatService.APP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败，抛出异常
        return response.json()
    
    @staticmethod
    def bind_phone(user_id, phone):
        """
        绑定手机号到微信用户
        :param user_id: 用户ID
        :param phone: 手机号
        :return: 更新后的用户信息
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception("用户不存在")
            
            # 检查手机号是否已被其他用户使用
            existing_user = User.query.filter_by(phone=phone).first()
            if existing_user and existing_user.id != user_id:
                raise Exception("该手机号已被其他用户绑定")
            
            user.phone = phone
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"绑定手机号失败: {str(e)}")
            raise Exception(f"绑定手机号失败: {str(e)}")
    
    @staticmethod
    def update_user_info(user_id, wechat_info):
        """
        更新微信用户信息
        :param user_id: 用户ID
        :param wechat_info: 微信用户信息
        :return: 更新后的用户信息
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception("用户不存在")
            
            # 更新用户信息
            if 'nickName' in wechat_info:
                user.wx_nickname = wechat_info['nickName']
                # 如果用户没有用户名，使用微信昵称作为用户名
                if not user.username or user.username.startswith('wx_'):
                    user.username = wechat_info['nickName']
            
            if 'avatarUrl' in wechat_info:
                user.wx_avatar_url = wechat_info['avatarUrl']
                # 如果用户没有头像，使用微信头像
                if not user.avatar:
                    user.avatar = wechat_info['avatarUrl']
            
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"更新微信用户信息失败: {str(e)}")
            raise Exception(f"更新用户信息失败: {str(e)}")
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.sms_service import SMSService
from app.services.wechat_service import WechatService
from app.utils.auth import token_required
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        # 获取请求数据
        data = request.get_json()
        logger.info(f"用户注册请求数据: {data}")
        
        # 验证请求数据格式
        if not data:
            logger.error("无效的请求格式: 没有JSON数据")
            return jsonify({'code': 400, 'message': '无效的请求格式'}), 400
        
        # 调用服务层进行注册
        user = UserService.register(data)
        
        # 返回成功响应
        response_data = {
            'code': 200,
            'message': '注册成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'phone': user.phone
            }
        }
        logger.info(f"用户注册成功: {user.id}")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        logger.info(f"用户登录请求数据: {data}")
        token = UserService.login(data)
        logger.info("用户登录成功")
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': token
            }
        })
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/send-sms-code', methods=['POST'])
def send_sms_code():
    """发送短信验证码"""
    try:
        data = request.get_json()
        if 'phone' not in data:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数: phone'
            }), 400
        
        phone = data['phone']
        logger.info(f"发送短信验证码请求: {phone}")
        
        # 生成并发送验证码
        code = SMSService.generate_code(phone)
        
        logger.info(f"短信验证码发送成功: {phone}")
        return jsonify({
            'code': 200,
            'message': '验证码发送成功'
        })
    except Exception as e:
        logger.error(f"发送短信验证码失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/login-with-sms', methods=['POST'])
def login_with_sms():
    """通过短信验证码登录"""
    try:
        data = request.get_json()
        logger.info(f"短信验证码登录请求数据: {data}")
        
        # 验证参数
        if 'phone' not in data or 'code' not in data:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数: phone或code'
            }), 400
        
        # 使用用户服务进行短信登录
        token = UserService.login_with_sms(data)
        
        logger.info("短信验证码登录成功")
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': token
            }
        })
    except Exception as e:
        logger.error(f"短信验证码登录失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/login-with-wechat', methods=['POST'])
def login_with_wechat():
    """通过微信登录"""
    try:
        data = request.get_json()
        logger.info(f"微信登录请求数据: {data}")
        
        # 验证参数
        if 'code' not in data:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数: code'
            }), 400
        
        code = data['code']
        token, user = WechatService.login_with_wechat(code)
        
        logger.info(f"微信登录成功，用户ID: {user.id}")
        return jsonify({
            'code': 200,
            'message': '微信登录成功',
            'data': {
                'access_token': token,
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'avatar': user.avatar,
                    'has_phone': bool(user.phone)
                }
            }
        })
    except Exception as e:
        logger.error(f"微信登录失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/bind-phone', methods=['POST'])
@token_required
def bind_phone(current_user):
    """微信用户绑定手机号"""
    try:
        data = request.get_json()
        logger.info(f"绑定手机号请求数据: {data}")
        
        # 验证参数
        if 'phone' not in data or 'code' not in data:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数: phone或code'
            }), 400
        
        # 验证短信验证码
        SMSService.verify_code(data['phone'], data['code'])
        
        # 绑定手机号
        user = WechatService.bind_phone(current_user.id, data['phone'])
        
        logger.info(f"手机号绑定成功，用户ID: {user.id}")
        return jsonify({
            'code': 200,
            'message': '手机号绑定成功',
            'data': {
                'phone': user.phone
            }
        })
    except Exception as e:
        logger.error(f"手机号绑定失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/update-wechat-info', methods=['POST'])
@token_required
def update_wechat_info(current_user):
    """更新微信用户信息"""
    try:
        data = request.get_json()
        logger.info(f"更新微信用户信息请求数据: {data}")
        
        # 验证参数
        if 'wechat_info' not in data:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数: wechat_info'
            }), 400
        
        # 更新用户信息
        user = WechatService.update_user_info(current_user.id, data['wechat_info'])
        
        logger.info(f"微信用户信息更新成功，用户ID: {user.id}")
        return jsonify({
            'code': 200,
            'message': '用户信息更新成功',
            'data': {
                'username': user.username,
                'avatar': user.avatar,
                'wx_nickname': user.wx_nickname
            }
        })
    except Exception as e:
        logger.error(f"微信用户信息更新失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

@user_bp.route('/info', methods=['GET'])
@token_required
def get_user_info(current_user):
    """获取用户信息"""
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'phone': current_user.phone,
            'email': current_user.email,
            'avatar': current_user.avatar
        }
    })

@user_bp.route('/addresses', methods=['GET'])
@token_required
def get_addresses(current_user):
    """获取用户地址列表"""
    addresses = UserService.get_user_addresses(current_user.id)
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [{
            'id': addr.id,
            'name': addr.name,
            'address': addr.address,
            'latitude': addr.latitude,
            'longitude': addr.longitude,
            'is_default': addr.is_default
        } for addr in addresses]
    })

@user_bp.route('/addresses', methods=['POST'])
@token_required
def add_address(current_user):
    """添加用户地址"""
    try:
        data = request.get_json()
        address = UserService.add_user_address(current_user.id, data)
        return jsonify({
            'code': 200,
            'message': '添加成功',
            'data': {
                'id': address.id,
                'name': address.name,
                'address': address.address,
                'latitude': address.latitude,
                'longitude': address.longitude,
                'is_default': address.is_default
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

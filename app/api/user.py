from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
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
        data = request.get_json()
        logger.info(f"用户注册请求数据: {data}")
        user = UserService.register(data)
        logger.info(f"用户注册成功: {user.id}")
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'phone': user.phone
            }
        })
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
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

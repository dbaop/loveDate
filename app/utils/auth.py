import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User


def generate_token(user_id):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    secret_key = current_app.config.get('JWT_SECRET_KEY', 'default-secret-key')
    return jwt.encode(payload, secret_key, algorithm='HS256')


def verify_token(token):
    """验证JWT token"""
    try:
        # 移除Bearer前缀
        if token.startswith('Bearer '):
            token = token[7:]
        secret_key = current_app.config.get('JWT_SECRET_KEY', 'default-secret-key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """装饰器：验证token"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 从请求头获取token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({
                'code': 401,
                'message': '缺少访问令牌'
            }), 401

        try:
            user_id = verify_token(token)
            if not user_id:
                return jsonify({
                    'code': 401,
                    'message': '令牌无效'
                }), 401

            current_user = User.query.filter_by(id=user_id).first()
            if not current_user:
                return jsonify({
                    'code': 401,
                    'message': '用户不存在'
                }), 401

        except Exception as e:
            return jsonify({
                'code': 401,
                'message': '令牌验证失败'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """装饰器：验证管理员权限"""

    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({
                'code': 403,
                'message': '权限不足，需要管理员权限'
            }), 403

        return f(current_user, *args, **kwargs)

    return decorated

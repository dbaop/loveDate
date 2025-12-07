from flask import Blueprint, request, jsonify
from app.services.message_service import MessageService
from app.utils.auth import token_required
from app.services.order_service import OrderService

message_bp = Blueprint('message', __name__)


@message_bp.route('/send', methods=['POST'])
@token_required
def send_message(current_user):
    """
    发送消息
    请求参数：
    {"receiver_id": 1, "receiver_role": "therapist", "order_id": 1, "content": "你好"}
    """
    try:
        data = request.get_json()
        
        # 获取参数
        receiver_id = data.get('receiver_id')
        receiver_role = data.get('receiver_role')
        order_id = data.get('order_id')
        content = data.get('content')
        
        # 验证参数
        if not all([receiver_id, receiver_role, order_id, content]):
            return jsonify({
                'code': 400,
                'message': '缺少必要参数'
            }), 400
        
        # 验证当前用户与订单的关系
        order = OrderService.get_order_detail(current_user.id, order_id)
        if not order:
            return jsonify({
                'code': 403,
                'message': '无权限操作此订单的消息'
            }), 403
        
        # 发送消息
        message = MessageService.send_message(
            sender_id=current_user.id,
            sender_role=current_user.role,
            receiver_id=receiver_id,
            receiver_role=receiver_role,
            order_id=order_id,
            content=content
        )
        
        return jsonify({
            'code': 200,
            'message': '消息发送成功',
            'data': message.to_dict()
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@message_bp.route('/history/<int:order_id>', methods=['GET'])
@token_required
def get_message_history(current_user):
    """
    获取消息历史记录
    请求参数：order_id（URL参数），page（查询参数，可选），size（查询参数，可选）
    """
    try:
        order_id = request.view_args.get('order_id')
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        
        # 验证当前用户与订单的关系
        order = OrderService.get_order_detail(current_user.id, order_id)
        if not order:
            return jsonify({
                'code': 403,
                'message': '无权限查看此订单的消息'
            }), 403
        
        # 获取消息历史
        result = MessageService.get_message_history(
            user_id=current_user.id,
            user_role=current_user.role,
            order_id=order_id,
            page=page,
            size=size
        )
        
        return jsonify({
            'code': 200,
            'message': '获取消息历史成功',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@message_bp.route('/unread-count', methods=['GET'])
@token_required
def get_unread_count(current_user):
    """
    获取未读消息数量
    """
    try:
        count = MessageService.get_unread_count(
            user_id=current_user.id,
            user_role=current_user.role
        )
        
        return jsonify({
            'code': 200,
            'message': '获取未读消息数量成功',
            'data': {
                'unread_count': count
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@message_bp.route('/mark-read/<int:message_id>', methods=['PUT'])
@token_required
def mark_message_as_read(current_user):
    """
    标记消息为已读
    """
    try:
        message_id = request.view_args.get('message_id')
        
        message = MessageService.mark_message_as_read(
            message_id=message_id,
            user_id=current_user.id,
            user_role=current_user.role
        )
        
        return jsonify({
            'code': 200,
            'message': '消息已标记为已读',
            'data': message.to_dict()
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@message_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversation_list(current_user):
    """
    获取会话列表
    """
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        
        result = MessageService.get_conversation_list(
            user_id=current_user.id,
            user_role=current_user.role,
            page=page,
            size=size
        )
        
        return jsonify({
            'code': 200,
            'message': '获取会话列表成功',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

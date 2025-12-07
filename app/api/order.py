from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
from app.utils.auth import token_required

order_bp = Blueprint('order', __name__)


@order_bp.route('/create', methods=['POST'])
@token_required
def create_order(current_user):
    """创建订单"""
    try:
        data = request.get_json()
        order = OrderService.create_order(current_user.id, data)
        return jsonify({
            'code': 200,
            'message': '订单创建成功',
            'data': {
                'id': order.id,
                'order_no': order.order_no,
                'status': order.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@order_bp.route('/list', methods=['GET'])
@token_required
def get_order_list(current_user):
    """获取订单列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    status = request.args.get('status', type=int)

    result = OrderService.get_user_orders(current_user.id, page, size, status)
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'items': [{
                'id': o.id,
                'order_no': o.order_no,
                'service_name': o.service_name,
                'price': o.price,
                'service_time': o.service_time.isoformat() if o.service_time else None,
                'status': o.status,
                'therapist_name': o.therapist.name if o.therapist else None,
                'therapist_avatar': o.therapist.avatar if o.therapist else None
            } for o in result['items']],
            'total': result['total'],
            'page': result['page'],
            'size': result['size']
        }
    })


@order_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order_detail(current_user, order_id):
    """获取订单详情"""
    order = OrderService.get_order_detail(current_user.id, order_id)
    if not order:
        return jsonify({
            'code': 404,
            'message': '订单不存在'
        }), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': order.id,
            'order_no': order.order_no,
            'service_name': order.service_name,
            'duration': order.duration,
            'price': order.price,
            'service_time': order.service_time.isoformat() if order.service_time else None,
            'service_address': order.service_address,
            'contact_phone': order.contact_phone,
            'status': order.status,
            'remark': order.remark,
            'created_at': order.created_at.isoformat(),
            'therapist': {
                'id': order.therapist.id,
                'name': order.therapist.name,
                'avatar': order.therapist.avatar,
                'phone': order.therapist.phone
            } if order.therapist else None
        }
    })


@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@token_required
def cancel_order(current_user, order_id):
    """取消订单"""
    try:
        OrderService.cancel_order(current_user.id, order_id)
        return jsonify({
            'code': 200,
            'message': '订单取消成功'
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


# 支付相关接口
@order_bp.route('/<int:order_id>/pay', methods=['POST'])
@token_required
def create_payment(current_user, order_id):
    """创建支付"""
    try:
        data = request.get_json()
        payment_method = data.get('payment_method', 'wechat')  # 默认微信支付
        result = OrderService.create_payment(order_id, current_user.id, payment_method)
        return jsonify({
            'code': 200,
            'message': '支付创建成功',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@order_bp.route('/<int:order_id>/payment/status', methods=['GET'])
@token_required
def get_payment_status(current_user, order_id):
    """查询支付状态"""
    try:
        status = OrderService.get_payment_status(order_id, current_user.id)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': status
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@order_bp.route('/payment/callback', methods=['POST'])
# 支付回调接口不需要token验证，需要验证支付平台的签名
# @token_required
def payment_callback():
    """支付回调处理"""
    try:
        # 实际应用中需要根据不同支付平台解析回调数据
        data = request.get_json() or request.form.to_dict()
        order = OrderService.payment_callback(data)
        return jsonify({
            'code': 200,
            'message': '回调处理成功',
            'data': {
                'order_no': order.order_no,
                'status': order.status,
                'payment_status': order.payment_status
            }
        })
    except Exception as e:
        # 即使处理失败，也需要返回成功的响应给支付平台
        # 否则支付平台会不断重试回调
        return jsonify({
            'code': 200,
            'message': '回调已接收',
            'error': str(e)
        })


@order_bp.route('/<int:order_id>/refund', methods=['POST'])
@token_required
def apply_refund(current_user, order_id):
    """申请退款"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        reason = data.get('reason', '用户申请退款')
        
        if not amount:
            raise Exception('退款金额不能为空')
        
        result = OrderService.refund(order_id, current_user.id, float(amount), reason)
        return jsonify({
            'code': 200,
            'message': '退款申请提交成功',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

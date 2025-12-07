from flask import Blueprint, request, jsonify
from app.services.feedback_service import FeedbackService
from app.utils.auth import token_required

feedback_bp = Blueprint('feedback', __name__)


@feedback_bp.route('/create', methods=['POST'])
@token_required
def create_feedback(current_user):
    """创建评价"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({
                'code': 400,
                'message': '订单ID不能为空'
            }), 400

        feedback = FeedbackService.create_feedback(current_user.id, order_id, data)
        return jsonify({
            'code': 200,
            'message': '评价创建成功',
            'data': {
                'id': feedback.id,
                'order_id': feedback.order_id,
                'rating': feedback.rating,
                'content': feedback.content,
                'tags': feedback.tags.split(',') if feedback.tags else [],
                'created_at': feedback.created_at.isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@feedback_bp.route('/therapist/<int:therapist_id>', methods=['GET'])
@token_required
def get_therapist_feedbacks(current_user, therapist_id):
    """获取技师的评价列表"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        result = FeedbackService.get_therapist_feedbacks(therapist_id, page, size)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'items': [{
                    'id': f.id,
                    'rating': f.rating,
                    'content': f.content,
                    'tags': f.tags.split(',') if f.tags else [],
                    'created_at': f.created_at.isoformat(),
                    'user_info': {
                        'username': f.user.username,
                        'avatar': f.user.avatar
                    }
                } for f in result['items']],
                'total': result['total'],
                'page': result['page'],
                'size': result['size']
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
@token_required
def get_feedback_detail(current_user, feedback_id):
    """获取评价详情"""
    try:
        feedback = FeedbackService.get_feedback_detail(feedback_id)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'id': feedback.id,
                'order_id': feedback.order_id,
                'rating': feedback.rating,
                'content': feedback.content,
                'tags': feedback.tags.split(',') if feedback.tags else [],
                'created_at': feedback.created_at.isoformat(),
                'user_info': {
                    'username': feedback.user.username,
                    'avatar': feedback.user.avatar
                },
                'therapist_info': {
                    'name': feedback.therapist.name,
                    'avatar': feedback.therapist.avatar
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@feedback_bp.route('/<int:feedback_id>/update', methods=['POST'])
@token_required
def update_feedback(current_user, feedback_id):
    """更新评价"""
    try:
        data = request.get_json()
        feedback = FeedbackService.update_feedback(current_user.id, feedback_id, data)
        return jsonify({
            'code': 200,
            'message': '评价更新成功',
            'data': {
                'id': feedback.id,
                'rating': feedback.rating,
                'content': feedback.content,
                'tags': feedback.tags.split(',') if feedback.tags else [],
                'updated_at': feedback.updated_at.isoformat() if feedback.updated_at else None
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@feedback_bp.route('/<int:feedback_id>/delete', methods=['POST'])
@token_required
def delete_feedback(current_user, feedback_id):
    """删除评价"""
    try:
        FeedbackService.delete_feedback(current_user.id, feedback_id)
        return jsonify({
            'code': 200,
            'message': '评价删除成功'
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@feedback_bp.route('/user/list', methods=['GET'])
@token_required
def get_user_feedbacks(current_user):
    """获取用户的评价历史"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        result = FeedbackService.get_user_feedbacks(current_user.id, page, size)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'items': [{
                    'id': f.id,
                    'rating': f.rating,
                    'content': f.content,
                    'tags': f.tags.split(',') if f.tags else [],
                    'created_at': f.created_at.isoformat(),
                    'therapist_info': {
                        'name': f.therapist.name,
                        'avatar': f.therapist.avatar
                    },
                    'service_name': f.order.service_name if f.order else None
                } for f in result['items']],
                'total': result['total'],
                'page': result['page'],
                'size': result['size']
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400
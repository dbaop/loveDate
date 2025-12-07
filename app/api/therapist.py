from flask import Blueprint, request, jsonify
from app.services.therapist_service import TherapistService
from app.services.order_service import OrderService
from app.utils.auth import token_required, admin_required
from app.utils.file_utils import handle_file_upload

therapist_bp = Blueprint('therapist', __name__)


@therapist_bp.route('/register', methods=['POST'])
def register():
    """技师注册"""
    try:
        
        # 获取表单数据
        data = request.form.to_dict()
        
        # 获取并处理上传的文件
        id_card_front = request.files.get('id_card_front')
        id_card_back = request.files.get('id_card_back')
        id_card_handheld = request.files.get('id_card_handheld')
        
        # 验证必填参数
        if not data.get('name'):
            return jsonify({
                'code': 400,
                'message': '姓名不能为空'
            }), 400
            
        if not data.get('phone'):
            return jsonify({
                'code': 400,
                'message': '手机号不能为空'
            }), 400
            
        if not data.get('id_card'):
            return jsonify({
                'code': 400,
                'message': '身份证号不能为空'
            }), 400
            
        # 验证身份证照片
        if not id_card_front or not id_card_back or not id_card_handheld:
            return jsonify({
                'code': 400,
                'message': '请上传身份证正反面和手持身份证照片'
            }), 400
        
        # 处理文件上传
        data['id_card_front'] = handle_file_upload(id_card_front)
        data['id_card_back'] = handle_file_upload(id_card_back)
        data['id_card_handheld'] = handle_file_upload(id_card_handheld)
        
        # 调用服务层注册技师
        therapist = TherapistService.register(data)
        
        return jsonify({
            'code': 200,
            'message': '注册成功，请等待管理员审核',
            'data': {
                'id': therapist.id,
                'name': therapist.name,
                'phone': therapist.phone,
                'status': therapist.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/list', methods=['GET'])
def get_therapists():
    """获取技师列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    keyword = request.args.get('keyword', '')

    result = TherapistService.get_list(page, size, keyword)
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'items': [{
                'id': t.id,
                'name': t.name,
                'age': t.age,
                'avatar': t.avatar,
                'rating': t.rating,
                'service_count': t.service_count,
                'specialty': t.specialty,
                'experience_years': t.experience_years
            } for t in result['items']],
            'total': result['total'],
            'page': result['page'],
            'size': result['size']
        }
    })


@therapist_bp.route('/<int:therapist_id>', methods=['GET'])
def get_therapist_detail(therapist_id):
    """获取技师详情"""
    therapist = TherapistService.get_detail(therapist_id)
    if not therapist:
        return jsonify({
            'code': 404,
            'message': '技师不存在'
        }), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': therapist.id,
            'name': therapist.name,
            'age': therapist.age,
            'avatar': therapist.avatar,
            'gender': therapist.gender,
            'rating': therapist.rating,
            'service_count': therapist.service_count,
            'specialty': therapist.specialty,
            'experience_years': therapist.experience_years,
            'introduction': therapist.introduction,
            'service_items': [{
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'duration': item.duration,
                'price': item.price
            } for item in therapist.service_items],
            'feedbacks': [{
                'id': f.id,
                'rating': f.rating,
                'content': f.content,
                'tags': f.tags.split(',') if f.tags else [],
                'created_at': f.created_at.isoformat(),
                'user_info': {
                    'username': f.user.username if f.user else '匿名用户',
                    'avatar': f.user.avatar if f.user else None
                }
            } for f in therapist.feedbacks[:3]]  # 返回前3条评价
        }
    })


@therapist_bp.route('/pending/list', methods=['GET'])
@token_required
@admin_required
def get_pending_therapists(current_user):
    """获取待审核技师列表"""
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        
        result = TherapistService.get_pending_list(page, size)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'items': [{
                    'id': t.id,
                    'name': t.name,
                    'phone': t.phone,
                    'gender': t.gender,
                    'id_card': t.id_card,
                    'id_card_front': t.id_card_front,
                    'id_card_back': t.id_card_back,
                    'id_card_handheld': t.id_card_handheld,
                    'experience_years': t.experience_years,
                    'specialty': t.specialty,
                    'created_at': t.created_at.isoformat() if hasattr(t, 'created_at') else None
                } for t in result['items']],
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


@therapist_bp.route('/<int:therapist_id>/approve', methods=['POST'])
@token_required
@admin_required
def approve_therapist(current_user, therapist_id):
    """审核通过技师"""
    try:
        therapist = TherapistService.approve_therapist(therapist_id)
        
        return jsonify({
            'code': 200,
            'message': '审核通过',
            'data': {
                'id': therapist.id,
                'name': therapist.name,
                'status': therapist.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/<int:therapist_id>/reject', methods=['POST'])
@token_required
@admin_required
def reject_therapist(current_user, therapist_id):
    """拒绝技师申请"""
    try:
        therapist = TherapistService.reject_therapist(therapist_id)
        
        return jsonify({
            'code': 200,
            'message': '已拒绝',
            'data': {
                'id': therapist.id,
                'name': therapist.name,
                'status': therapist.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/my/services', methods=['GET'])
@token_required  # 需要验证用户身份
def get_my_services(current_user):
    """获取当前登录治疗师的专属服务套餐列表"""
    # 检查用户是否是治疗师
    if current_user.role != 'therapist':
        return jsonify({
            'code': 403,
            'message': '权限不足，需要治疗师权限'
        }), 403
    
    # 获取治疗师信息
    therapist = TherapistService.get_therapist_by_user_id(current_user.id)
    if not therapist:
        return jsonify({
            'code': 404,
            'message': '治疗师信息不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'therapist_id': therapist.id,
            'therapist_name': therapist.name,
            'services': [{
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'duration': item.duration,
                'price': item.price,
                'category': item.category
            } for item in therapist.service_items]
        }
    })

# 技师端订单管理接口
@therapist_bp.route('/orders', methods=['GET'])
@token_required  # 需要验证技师身份
# 这里需要添加技师身份验证
# @therapist_required
def get_therapist_orders(current_user):
    """获取技师订单列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    status = request.args.get('status', type=int)
    
    # 这里假设current_user是技师
    # 实际应用中需要添加技师身份验证和关联
    result = OrderService.get_therapist_orders(current_user.id, page, size, status)
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
                'user_name': o.user.username if o.user else None,
                'service_address': o.service_address,
                'contact_phone': o.contact_phone
            } for o in result['items']],
            'total': result['total'],
            'page': result['page'],
            'size': result['size']
        }
    })


@therapist_bp.route('/orders/<int:order_id>/accept', methods=['POST'])
@token_required  # 需要验证技师身份
# @therapist_required
def accept_order(current_user, order_id):
    """接受订单"""
    try:
        order = OrderService.accept_order(current_user.id, order_id)
        return jsonify({
            'code': 200,
            'message': '订单接受成功',
            'data': {
                'id': order.id,
                'status': order.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/orders/<int:order_id>/journey', methods=['POST'])
@token_required  # 需要验证技师身份
# @therapist_required
def start_journey(current_user, order_id):
    """技师出发"""
    try:
        order = OrderService.start_journey(current_user.id, order_id)
        return jsonify({
            'code': 200,
            'message': '已确认出发',
            'data': {
                'id': order.id,
                'status': order.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/orders/<int:order_id>/start', methods=['POST'])
@token_required  # 需要验证技师身份
# @therapist_required
def start_service(current_user, order_id):
    """开始服务"""
    try:
        order = OrderService.start_service(current_user.id, order_id)
        return jsonify({
            'code': 200,
            'message': '服务已开始',
            'data': {
                'id': order.id,
                'status': order.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@therapist_bp.route('/orders/<int:order_id>/complete', methods=['POST'])
@token_required  # 需要验证技师身份
# @therapist_required
def complete_order(current_user, order_id):
    """完成服务"""
    try:
        order = OrderService.complete_order(current_user.id, order_id)
        return jsonify({
            'code': 200,
            'message': '服务已完成',
            'data': {
                'id': order.id,
                'status': order.status
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400

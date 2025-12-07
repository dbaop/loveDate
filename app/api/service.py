from flask import Blueprint, request, jsonify
from app.services.therapist_service import TherapistService
from app.utils.auth import token_required, admin_required

service_bp = Blueprint('service', __name__)


@service_bp.route('/items', methods=['GET'])
def get_service_items():
    """获取服务项目列表"""
    category = request.args.get('category')
    service_items = TherapistService.get_service_items(category)
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [{
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'duration': item.duration,
            'price': item.price,
            'category': item.category
        } for item in service_items]
    })


@service_bp.route('/items/<int:item_id>', methods=['GET'])
def get_service_item_detail(item_id):
    """获取服务项目详情"""
    item = TherapistService.get_service_item_detail(item_id)
    if not item:
        return jsonify({
            'code': 404,
            'message': '服务项目不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'duration': item.duration,
            'price': item.price,
            'category': item.category
        }
    })


@service_bp.route('/items', methods=['POST'])
@token_required  # 验证用户已登录
@admin_required  # 验证管理员权限
def create_service_item(current_user):
    """创建服务项目"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        data = request.get_json()
        logger.info(f"创建服务项目收到的数据: {data}")
        logger.info(f"数据类型: {type(data)}")
        logger.info(f"duration字段类型: {type(data.get('duration'))}")
        
        service_item = TherapistService.create_service_item(data)
        return jsonify({
            'code': 200,
            'message': '服务项目创建成功',
            'data': {
                'id': service_item.id,
                'name': service_item.name
            }
        })
    except Exception as e:
        logger.error(f"创建服务项目失败: {str(e)}")
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@service_bp.route('/items/<int:item_id>', methods=['PUT'])
@token_required  # 验证用户已登录
@admin_required  # 验证管理员权限
def update_service_item(current_user, item_id):
    """更新服务项目"""
    try:
        data = request.get_json()
        service_item = TherapistService.update_service_item(item_id, data)
        return jsonify({
            'code': 200,
            'message': '服务项目更新成功',
            'data': {
                'id': service_item.id,
                'name': service_item.name
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@service_bp.route('/items/<int:item_id>', methods=['DELETE'])
@token_required  # 验证用户已登录
@admin_required  # 验证管理员权限
def delete_service_item(current_user, item_id):
    """删除服务项目"""
    try:
        TherapistService.delete_service_item(item_id)
        return jsonify({
            'code': 200,
            'message': '服务项目删除成功'
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400


@service_bp.route('/therapists/<int:therapist_id>/services', methods=['POST'])
@token_required  # 验证用户已登录
@admin_required  # 验证管理员权限
def assign_services_to_therapist(current_user, therapist_id):
    """为技师分配服务项目"""
    try:
        data = request.get_json()
        service_item_ids = data['service_item_ids']
        therapist = TherapistService.assign_services_to_therapist(therapist_id, service_item_ids)
        return jsonify({
            'code': 200,
            'message': '服务项目分配成功',
            'data': {
                'therapist_id': therapist.id,
                'service_count': len(therapist.service_items)
            }
        })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400
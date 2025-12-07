from app.models.therapist import Therapist, ServiceItem
from app.models.user import User
from app import db


class TherapistService:
    @staticmethod
    def register(data):
        """技师注册"""
        # 检查手机号是否已存在
        existing_therapist = Therapist.query.filter_by(phone=data['phone']).first()
        if existing_therapist:
            raise Exception("手机号已注册")

        # 创建技师（直接通过审核）
        therapist = Therapist(
            name=data['name'],
            phone=data['phone'],
            id_card=data.get('id_card'),
            certification=data.get('certification'),
            experience_years=data.get('experience_years'),
            specialty=data.get('specialty'),
            introduction=data.get('introduction'),
            status=1  # 直接设置为正常状态
        )

        db.session.add(therapist)
        db.session.commit()
        return therapist

    @staticmethod
    def get_list(page, size, keyword=''):
        """获取技师列表"""
        query = Therapist.query.filter_by(status=1)  # 只查询审核通过的技师

        if keyword:
            query = query.filter(Therapist.name.contains(keyword))

        # 按评分和接单数排序
        query = query.order_by(Therapist.rating.desc(), Therapist.service_count.desc())

        # 分页
        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'size': size
        }

    @staticmethod
    def get_detail(therapist_id):
        """获取技师详情"""
        return Therapist.query.filter_by(id=therapist_id, status=1).first()

    # 服务项目管理
    @staticmethod
    def create_service_item(data):
        """创建服务项目"""
        # 确保必要参数存在
        if not data.get('name'):
            raise Exception("服务名称不能为空")
        if not data.get('price'):
            raise Exception("服务价格不能为空")
        if not data.get('duration'):
            raise Exception("服务时长不能为空")
        
        # 转换参数类型
        try:
            duration = int(data['duration'])
            price = float(data['price'])
        except ValueError:
            raise Exception("参数类型错误：时长必须是整数，价格必须是数字")
            
        service_item = ServiceItem(
            name=data['name'],
            description=data.get('description'),
            duration=duration,
            price=price,
            category=data.get('category', 'classic')
        )
        db.session.add(service_item)
        db.session.commit()
        return service_item

    @staticmethod
    def get_service_items(category=None):
        """获取服务项目列表"""
        query = ServiceItem.query.filter_by(status=1)
        if category:
            query = query.filter_by(category=category)
        return query.all()

    @staticmethod
    def get_service_item_detail(item_id):
        """获取服务项目详情"""
        return ServiceItem.query.filter_by(id=item_id, status=1).first()

    @staticmethod
    def update_service_item(item_id, data):
        """更新服务项目"""
        service_item = ServiceItem.query.get(item_id)
        if not service_item:
            raise Exception("服务项目不存在")
        
        if 'name' in data:
            service_item.name = data['name']
        if 'description' in data:
            service_item.description = data['description']
        if 'duration' in data:
            service_item.duration = data['duration']
        if 'price' in data:
            service_item.price = data['price']
        if 'category' in data:
            service_item.category = data['category']
        if 'status' in data:
            service_item.status = data['status']
        
        db.session.commit()
        return service_item

    @staticmethod
    def delete_service_item(item_id):
        """删除服务项目"""
        service_item = ServiceItem.query.get(item_id)
        if not service_item:
            raise Exception("服务项目不存在")
        
        service_item.status = 0  # 软删除
        db.session.commit()
        return service_item

    @staticmethod
    def assign_services_to_therapist(therapist_id, service_item_ids):
        """为技师分配服务项目"""
        therapist = Therapist.query.get(therapist_id)
        if not therapist:
            raise Exception("技师不存在")
        
        # 清除现有服务项目
        therapist.service_items = []
        
        # 添加新的服务项目
        for item_id in service_item_ids:
            service_item = ServiceItem.query.get(item_id)
            if service_item:
                therapist.service_items.append(service_item)
        
        db.session.commit()
        return therapist
    
    @staticmethod
    def get_therapist_by_user_id(user_id):
        """通过用户ID获取治疗师信息"""
        # 目前治疗师和用户是分开的表，这里假设治疗师的phone和用户的phone一致
        # 后续可以考虑在治疗师表中添加user_id字段来建立直接关联
        user = User.query.get(user_id)
        if not user:
            return None
        
        return Therapist.query.filter_by(phone=user.phone).first()

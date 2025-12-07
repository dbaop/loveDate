from app.models.message import Message
from app import db
from datetime import datetime


class MessageService:
    @staticmethod
    def send_message(sender_id, sender_role, receiver_id, receiver_role, order_id, content):
        """
        发送消息
        :param sender_id: 发送者ID
        :param sender_role: 发送者角色 (user/therapist)
        :param receiver_id: 接收者ID
        :param receiver_role: 接收者角色 (user/therapist)
        :param order_id: 关联的订单ID
        :param content: 消息内容
        :return: 创建的消息对象
        """
        # 验证参数
        if not all([sender_id, sender_role, receiver_id, receiver_role, order_id, content]):
            raise ValueError("缺少必要参数")
        
        if sender_role not in ['user', 'therapist'] or receiver_role not in ['user', 'therapist']:
            raise ValueError("角色参数错误")
        
        # 创建消息
        message = Message(
            sender_id=sender_id,
            sender_role=sender_role,
            receiver_id=receiver_id,
            receiver_role=receiver_role,
            order_id=order_id,
            content=content,
            is_read=False,
            created_at=datetime.now()
        )
        
        db.session.add(message)
        db.session.commit()
        
        return message
    
    @staticmethod
    def get_message_history(user_id, user_role, order_id, page=1, size=20):
        """
        获取消息历史记录
        :param user_id: 用户ID
        :param user_role: 用户角色 (user/therapist)
        :param order_id: 订单ID
        :param page: 页码
        :param size: 每页大小
        :return: 消息列表和分页信息
        """
        # 构建查询条件
        query = Message.query.filter_by(order_id=order_id)
        query = query.filter(
            ((Message.sender_id == user_id) & (Message.sender_role == user_role)) |
            ((Message.receiver_id == user_id) & (Message.receiver_role == user_role))
        )
        
        # 按时间降序排序，最新的消息在最后
        query = query.order_by(Message.created_at.asc())
        
        # 分页查询
        pagination = query.paginate(page=page, per_page=size, error_out=False)
        
        # 标记当前用户收到的消息为已读
        unread_messages = Message.query.filter_by(
            receiver_id=user_id,
            receiver_role=user_role,
            order_id=order_id,
            is_read=False
        ).all()
        
        for msg in unread_messages:
            msg.is_read = True
        
        db.session.commit()
        
        return {
            'items': [msg.to_dict() for msg in pagination.items],
            'total': pagination.total,
            'page': page,
            'size': size
        }
    
    @staticmethod
    def get_unread_count(user_id, user_role):
        """
        获取未读消息数量
        :param user_id: 用户ID
        :param user_role: 用户角色 (user/therapist)
        :return: 未读消息数量
        """
        count = Message.query.filter_by(
            receiver_id=user_id,
            receiver_role=user_role,
            is_read=False
        ).count()
        
        return count
    
    @staticmethod
    def mark_message_as_read(message_id, user_id, user_role):
        """
        标记消息为已读
        :param message_id: 消息ID
        :param user_id: 用户ID
        :param user_role: 用户角色 (user/therapist)
        :return: 更新后的消息对象
        """
        message = Message.query.get(message_id)
        
        if not message:
            raise ValueError("消息不存在")
        
        # 验证消息接收者
        if message.receiver_id != user_id or message.receiver_role != user_role:
            raise ValueError("无权限操作此消息")
        
        message.is_read = True
        db.session.commit()
        
        return message
    
    @staticmethod
    def get_conversation_list(user_id, user_role, page=1, size=10):
        """
        获取会话列表（按订单分组的最新消息）
        :param user_id: 用户ID
        :param user_role: 用户角色 (user/therapist)
        :param page: 页码
        :param size: 每页大小
        :return: 会话列表和分页信息
        """
        # 首先获取用户参与的所有订单ID
        from app.models.order import Order
        
        if user_role == 'user':
            order_query = Order.query.filter_by(user_id=user_id)
        else:  # therapist
            order_query = Order.query.filter_by(therapist_id=user_id)
        
        # 获取最新消息
        # 这里使用子查询获取每个订单的最新消息
        subquery = db.session.query(
            Message.order_id,
            db.func.max(Message.created_at).label('max_created_at')
        ).filter(
            ((Message.sender_id == user_id) & (Message.sender_role == user_role)) |
            ((Message.receiver_id == user_id) & (Message.receiver_role == user_role))
        ).group_by(Message.order_id).subquery()
        
        # 主查询
        query = db.session.query(Message).join(
            subquery,
            (Message.order_id == subquery.c.order_id) & 
            (Message.created_at == subquery.c.max_created_at)
        ).order_by(Message.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=size, error_out=False)
        
        return {
            'items': [msg.to_dict() for msg in pagination.items],
            'total': pagination.total,
            'page': page,
            'size': size
        }

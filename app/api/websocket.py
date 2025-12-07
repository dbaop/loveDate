from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
import json
from datetime import datetime
from app.utils.auth import verify_token

# 创建SocketIO实例（将在main.py中初始化）
socketio = SocketIO(logger=True, engineio_logger=True)

# 用户ID与socket ID的映射
user_sockets = {}

@socketio.on('connect')
def handle_connect():
    """处理WebSocket连接"""
    # 从查询参数中获取token
    token = request.args.get('token')
    print(f"WebSocket连接请求，token: {token}")
    if not token:
        print(f"WebSocket连接失败：缺少token参数")
        emit('connect_error', {'message': '缺少认证token'})
        return False
    
    try:
        # 验证并解码token
        user_id = verify_token(token)
        
        if not user_id:
            print(f"WebSocket连接失败：token无效 {token}")
            emit('connect_error', {'message': 'token无效'})
            return False
        
        print(f"验证token成功，user_id: {user_id}")
        
        # 保存用户ID与socket ID的映射
        user_sockets[user_id] = request.sid
        print(f"保存用户映射: {user_id} -> {request.sid}")
        print(f"当前用户映射: {user_sockets}")
        
        # 让用户加入自己的房间
        join_room(user_id)
        
        emit('connected', {'message': '连接成功'})
        return True
    except Exception as e:
        print(f"WebSocket连接异常：{str(e)}")
        emit('connect_error', {'message': str(e)})
        return False

@socketio.on('disconnect')
def handle_disconnect():
    """处理WebSocket断开连接"""
    # 从user_sockets中移除断开连接的用户
    for user_id, sid in user_sockets.items():
        if sid == request.sid:
            del user_sockets[user_id]
            leave_room(user_id)
            break

@socketio.on('send_message')
def handle_send_message(data):
    """处理发送消息事件"""
    try:
        print(f"接收到send_message事件，数据: {data}")
        print(f"当前socket ID: {request.sid}")
        print(f"当前用户映射: {user_sockets}")
        
        # 获取当前用户ID（从连接时保存的映射中获取）
        current_user_id = None
        for user_id, sid in user_sockets.items():
            print(f"检查: user_id={user_id}, sid={sid}, request.sid={request.sid}")
            if sid == request.sid:
                current_user_id = user_id
                break
        
        if not current_user_id:
            print("未找到匹配的用户ID")
            emit('error', {'message': '未认证的连接'})
            return
        
        # 验证消息数据
        required_fields = ['receiver_id', 'receiver_role', 'order_id', 'content']
        if not all(field in data for field in required_fields):
            emit('error', {'message': '缺少必要参数'})
            return
        
        # 这里可以添加消息处理逻辑，例如保存到数据库等
        # 然后将消息发送给接收者
        receiver_id = data['receiver_id']
        
        # 构建消息对象
        message = {
            'sender_id': current_user_id,
            'sender_role': data.get('sender_role', 'user'),
            'receiver_id': receiver_id,
            'receiver_role': data['receiver_role'],
            'order_id': data['order_id'],
            'content': data['content'],
            'created_at': data.get('created_at', str(datetime.now()))
        }
        
        # 如果接收者在线，发送消息
        if receiver_id in user_sockets:
            emit('new_message', message, room=receiver_id)
        
        # 确认消息发送成功
        emit('message_sent', {'message': '消息发送成功', 'data': message})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('join_order_room')
def handle_join_order_room(data):
    """加入订单聊天房间"""
    try:
        order_id = data.get('order_id')
        if not order_id:
            emit('error', {'message': '缺少订单ID'})
            return
        
        # 加入订单房间
        join_room(f'order_{order_id}')
        emit('joined_room', {'message': f'已加入订单{order_id}的聊天房间'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('leave_order_room')
def handle_leave_order_room(data):
    """离开订单聊天房间"""
    try:
        order_id = data.get('order_id')
        if not order_id:
            emit('error', {'message': '缺少订单ID'})
            return
        
        # 离开订单房间
        leave_room(f'order_{order_id}')
        emit('left_room', {'message': f'已离开订单{order_id}的聊天房间'})
    except Exception as e:
        emit('error', {'message': str(e)})

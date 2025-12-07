import socketio
import time

# 创建Socket.IO客户端实例
sio = socketio.Client()

# 事件处理函数
@sio.event
def connect():
    print('连接成功')
    
    # 发送测试消息
    test_message = {
        'receiver_id': 2,
        'receiver_role': 'therapist',
        'order_id': 1,
        'content': '测试消息'
    }
    sio.emit('send_message', test_message)
    print(f'发送测试消息: {test_message}')

@sio.event
def connect_error(error):
    print(f'连接错误: {error}')

@sio.event
def disconnect():
    print('连接断开')

@sio.event
def connected(data):
    print(f'服务器确认连接: {data}')

@sio.event
def message_sent(data):
    print(f'消息发送成功: {data}')

@sio.event
def error(data):
    print(f'服务器错误: {data}')

# 生成测试token
def generate_test_token():
    import jwt
    import datetime
    
    # 使用与后端开发环境相同的JWT密钥
    secret_key = 'dev-secret-key-for-websocket-testing'  # 与config.py中的DevelopmentConfig.JWT_SECRET_KEY一致
    payload = {
        'user_id': 1,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# 连接到服务器
try:
    token = generate_test_token()
    print(f'生成的测试token: {token}')
    
    # 连接到Socket.IO服务器，将token参数直接添加到URL中
    sio.connect(
        f'http://localhost:5000?token={token}',
        transports=['websocket'],
        wait=True
    )
    
    # 保持连接
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print('测试结束')
    sio.disconnect()
except Exception as e:
    print(f'连接异常: {e}')
    import traceback
    traceback.print_exc()

import socketio
import time

# 创建SocketIO客户端
sio = socketio.Client()

# 事件处理函数
@sio.event
def connect():
    print("WebSocket连接成功")
    
    # 发送测试消息
    test_message = {
        'receiver_id': 2,  # 假设接收者ID为2
        'receiver_role': 'therapist',
        'order_id': 1,     # 假设订单ID为1
        'content': '这是一条测试消息'
    }
    sio.emit('send_message', test_message)

@sio.event
def connect_error(error):
    print(f"WebSocket连接错误: {error}")

@sio.event
def disconnect():
    print("WebSocket断开连接")

@sio.event
def connected(data):
    print(f"已连接: {data}")

@sio.event
def message_sent(data):
    print(f"消息发送成功: {data}")

@sio.event
def new_message(data):
    print(f"收到新消息: {data}")

@sio.event
def error(data):
    print(f"错误: {data}")

if __name__ == '__main__':
    try:
        # 使用最新的token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTE2Mzl9.9P6qQqfR-peACXQB9L1ikqrUoOrDbBw6pFIL_8cnsPY'
        # 连接WebSocket服务
        url = f'http://localhost:5000?token={token}'
        print(f'连接URL: {url}')
        sio.connect(url, socketio_path='/api/ws')
        
        # 保持连接10秒
        time.sleep(10)
        
        # 断开连接
        sio.disconnect()
    except Exception as e:
        print(f"测试错误: {e}")
import socketio
import time

# 使用最新的token
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTE2Mzl9.9P6qQqfR-peACXQB9L1ikqrUoOrDbBw6pFIL_8cnsPY'

# 创建SocketIO客户端
sio = socketio.Client()

@sio.event
def connect():
    print('WebSocket连接成功')

@sio.event
def connect_error(data):
    print(f'WebSocket连接错误: {data}')

@sio.event
def disconnect():
    print('WebSocket断开连接')

@sio.event
def message_sent(data):
    print(f'消息发送成功: {data}')

if __name__ == '__main__':
    try:
        # 连接WebSocket服务
        url = f'http://localhost:5000?token={token}'
        print(f'连接URL: {url}')
        sio.connect(url, socketio_path='/api/ws')
        
        # 发送测试消息
        sio.emit('send_message', {
            'receiver_id': 2,
            'receiver_role': 'therapist',
            'order_id': 1,
            'content': '这是一条测试消息'
        })
        
        # 等待3秒后断开连接
        time.sleep(3)
        sio.disconnect()
    except Exception as e:
        print(f'测试过程中出现错误: {e}')

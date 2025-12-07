import sys
import os
import time
import json

# 添加项目路径
sys.path.append(os.path.abspath('.'))

# 生成测试token
from flask import Flask
from app.utils.auth import generate_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'default-secret-key'

with app.app_context():
    token = generate_token(1)
    print(f"测试token: {token}")

# 测试WebSocket连接
print("\n正在测试WebSocket连接...")

# 使用websocket-client库
from websocket import create_connection

ws_url = f"ws://localhost:5000/socket.io/?token={token}&transport=websocket"
print(f"WebSocket URL: {ws_url}")

try:
    ws = create_connection(ws_url)
    print("WebSocket连接成功!")
    
    # 接收连接响应
    result = ws.recv()
    print(f"收到连接响应: {result}")
    
    # 发送测试消息
    test_message = {
        "receiver_id": 2,
        "receiver_role": "therapist",
        "order_id": 1,
        "content": "测试消息"
    }
    
    # 使用socketio的消息格式
    message = {
        "type": "send_message",
        "data": test_message
    }
    
    ws.send(json.dumps(message))
    print("发送测试消息")
    
    # 接收响应
    result = ws.recv()
    print(f"收到消息响应: {result}")
    
    # 关闭连接
    ws.close()
    print("WebSocket连接关闭")
    
except Exception as e:
    print(f"WebSocket连接失败: {e}")
    import traceback
    traceback.print_exc()

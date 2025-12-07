import sys
import os
import json

# 添加项目路径
sys.path.append(os.path.abspath('.'))

from flask import Flask
from app.api.websocket import socketio
from app.utils.auth import generate_token

# 创建Flask应用
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'default-secret-key'

# 初始化SocketIO
socketio.init_app(app, cors_allowed_origins="*")

# 生成测试token
with app.app_context():
    token = generate_token(1)
    print(f"测试token: {token}")
    print(f"WebSocket URL: ws://localhost:5000/api/ws?token={token}")

print("\n请使用以下命令启动服务器：")
print("python main.py")
print("\n然后使用WebSocket客户端测试连接")

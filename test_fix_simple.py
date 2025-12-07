import requests
import socketio
import time
import sys
import os

# 测试参数
BASE_URL = 'http://localhost:5000'
WS_URL = 'ws://localhost:5000/api/ws'
USER_ID = 1  # 使用已知的用户ID

def get_token():
    """获取token的简单方法：从test_frontend_api.py中复制一个有效的token"""
    # 从之前的测试中获取一个有效的token
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTE2Mzl9.9P6qQqfR-peACXQB9L1ikqrUoOrDbBw6pFIL_8cnsPY"

def test_message_list_api(token):
    """测试消息列表API"""
    print("\n=== 测试消息列表API ===")
    url = f'{BASE_URL}/api/message/list'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 检查数据结构
    data = response.json()
    if 'data' in data and isinstance(data['data'], list):
        print("✓ 消息列表数据结构正确")
    else:
        print("✗ 消息列表数据结构错误")

def test_websocket_connection(token):
    """测试WebSocket连接"""
    print("\n=== 测试WebSocket连接 ===")
    
    # 创建SocketIO客户端
    sio = socketio.Client()
    
    # 事件处理函数
    @sio.on('connect')
    def on_connect():
        print("✓ WebSocket连接成功")
    
    @sio.on('connected')
    def on_connected(data):
        print(f"✓ 接收到connected事件: {data}")
    
    @sio.on('connect_error')
    def on_connect_error(data):
        print(f"✗ WebSocket连接错误: {data}")
    
    @sio.on('error')
    def on_error(data):
        print(f"✗ WebSocket错误: {data}")
    
    try:
        # 连接WebSocket服务器，将token作为URL参数传递
        ws_url_with_token = f"{WS_URL}?token={token}"
        print(f"正在连接WebSocket: {ws_url_with_token}")
        sio.connect(ws_url_with_token, transports=['websocket'])
        
        # 保持连接一段时间
        time.sleep(2)
        
        # 断开连接
        sio.disconnect()
        print("✓ WebSocket断开连接")
        return True
    except Exception as e:
        print(f"✗ WebSocket连接异常: {e}")
        return False

def test_conversation_api(token):
    """测试会话列表API（原始）"""
    print("\n=== 测试会话列表API（原始） ===")
    url = f'{BASE_URL}/api/message/conversations'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")

if __name__ == '__main__':
    # 获取token
    token = get_token()
    if token:
        print(f"\n使用的token: {token}")
        
        # 测试API
        test_conversation_api(token)  # 测试原始会话列表API
        test_message_list_api(token)  # 测试修改后的消息列表API
        
        # 测试WebSocket
        test_websocket_connection(token)
    else:
        print("无法获取token，测试失败")
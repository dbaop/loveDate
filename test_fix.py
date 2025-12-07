import requests
import socketio
import time

# 测试参数
BASE_URL = 'http://localhost:5000'
WS_URL = 'ws://localhost:5000/api/ws'

# 首先登录获取token
def get_token():
    url = f'{BASE_URL}/api/user/login-with-sms'
    data = {
        'phone': '13800138000',
        'code': '123456'
    }
    response = requests.post(url, json=data)
    print(f"登录请求响应: {response.text}")
    if response.status_code == 200:
        return response.json()['data']['access_token']
    else:
        print(f"获取token失败: {response.text}")
        return None

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
        # 连接WebSocket服务器
        print(f"正在连接WebSocket: {WS_URL}?token={token}")
        sio.connect(WS_URL, transports=['websocket'], query={'token': token})
        
        # 保持连接一段时间
        time.sleep(2)
        
        # 断开连接
        sio.disconnect()
        print("✓ WebSocket断开连接")
        return True
    except Exception as e:
        print(f"✗ WebSocket连接异常: {e}")
        return False

if __name__ == '__main__':
    # 获取token
    token = get_token()
    if token:
        print(f"获取到token: {token}")
        
        # 测试API
        test_message_list_api(token)
        
        # 测试WebSocket
        test_websocket_connection(token)
    else:
        print("无法获取token，测试失败")
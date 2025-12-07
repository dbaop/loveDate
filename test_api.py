import requests
import json

# 登录获取JWT令牌
def login_with_code():
    url = 'http://localhost:5000/api/user/login'
    headers = {'Content-Type': 'application/json'}
    data = {
        'phone': '13621114638',
        'code': '955031'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f'Login Status Code: {response.status_code}')
        print(f'Login Response: {response.text}')
        
        if response.status_code == 200:
            return response.json().get('data', {}).get('access_token')
        return None
    except Exception as e:
        print(f'Login Error: {e}')
        return None

# 测试 /api/message/unread 接口
def test_unread_api(token):
    url = 'http://localhost:5000/api/message/unread'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f'\nUnread API Status Code: {response.status_code}')
        print(f'Unread API Response: {response.text}')
        return response.status_code
    except Exception as e:
        print(f'\nUnread API Error: {e}')
        return None

# 测试 /api/message/list 接口
def test_message_list_api(token):
    url = 'http://localhost:5000/api/message/list'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f'\nMessage List API Status Code: {response.status_code}')
        print(f'Message List API Response: {response.text}')
        return response.status_code
    except Exception as e:
        print(f'\nMessage List API Error: {e}')
        return None

if __name__ == '__main__':
    # 获取JWT令牌
    token = login_with_code()
    
    if token:
        print(f'\n获取到的Token: {token}')
        
        # 测试API接口
        test_unread_api(token)
        test_message_list_api(token)
    else:
        print('获取Token失败')
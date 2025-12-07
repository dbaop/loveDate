import requests
import json

# 发送短信验证码
def send_sms_code():
    url = 'http://localhost:5000/api/user/send-sms-code'
    headers = {'Content-Type': 'application/json'}
    data = {'phone': '13621114638'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f'HTTP Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json()
    except Exception as e:
        print(f'Error: {e}')
        return None

if __name__ == '__main__':
    send_sms_code()
import requests

# 使用最新的token
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTE2Mzl9.9P6qQqfR-peACXQB9L1ikqrUoOrDbBw6pFIL_8cnsPY'

# 测试未读消息API
print("测试未读消息API...")
unread_url = "http://localhost:5000/api/message/unread"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(unread_url, headers=headers)
print(f"未读消息API状态码: {response.status_code}")
print(f"未读消息API响应: {response.json()}")
print()

# 测试消息列表API
print("测试消息列表API...")
message_list_url = "http://localhost:5000/api/message/list"
response = requests.get(message_list_url, headers=headers)
print(f"消息列表API状态码: {response.status_code}")
print(f"消息列表API响应: {response.json()}")
print()

# 测试没有Authorization头的情况
print("测试没有Authorization头的情况...")
response = requests.get(unread_url)
print(f"未授权请求状态码: {response.status_code}")
print(f"未授权请求响应: {response.json()}")
print()

# 测试使用错误token的情况
print("测试使用错误token的情况...")
invalid_headers = {
    "Authorization": "Bearer invalid_token"
}
response = requests.get(unread_url, headers=invalid_headers)
print(f"错误token请求状态码: {response.status_code}")
print(f"错误token请求响应: {response.json()}")

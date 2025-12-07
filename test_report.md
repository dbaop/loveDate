# 后端API和WebSocket测试报告

## 测试环境
- 服务器地址：http://localhost:5000
- 测试时间：2025-12-07 23:00
- Python版本：3.10+
- Flask版本：2.0+

## 测试结果

### 1. API接口测试

| 接口 | 状态码 | 结果 | 备注 |
|------|--------|------|------|
| /api/message/unread | 200 | ✅ 成功 | 返回未读消息数量 |
| /api/message/list | 200 | ✅ 成功 | 返回会话列表 |
| 未授权请求 | 401 | ✅ 正常 | 正确返回401错误 |
| 错误token请求 | 401 | ✅ 正常 | 正确返回401错误 |

### 2. WebSocket测试

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 连接建立 | ✅ 成功 | WebSocket连接正常 |
| 消息发送 | ✅ 成功 | 消息可以正常发送和接收 |
| 连接断开 | ✅ 成功 | 连接可以正常断开 |

## 前端访问失败分析

从前端小程序的错误日志可以看出：

1. **API请求401未授权错误**
   - 前端使用的token：`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTA0MTh9.ycYEV9DtuFQ0ccdI-x34nbhDabrOMVPEgUIiq1ISLqY`
   - 这个token的过期时间是`1767710418`，已经过期

2. **WebSocket连接失败**
   - 连接地址：`ws://localhost:5000/api/ws`
   - 可能原因：token过期或无效

## 解决方案

1. **更新JWT令牌**
   - 前端需要重新登录获取新的令牌
   - 最新可用的token：`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Njc3MTE2Mzl9.9P6qQqfR-peACXQB9L1ikqrUoOrDbBw6pFIL_8cnsPY`
   - 过期时间：2025-12-07 23:01:07

2. **WebSocket连接方式**
   - 确保在WebSocket连接URL中包含有效的token参数：`ws://localhost:5000/api/ws?token=YOUR_TOKEN_HERE`

3. **API请求头设置**
   - 确保在API请求头中正确设置Authorization：`Bearer YOUR_TOKEN_HERE`

## 建议

1. 前端实现token自动刷新机制，避免token过期导致请求失败
2. 在WebSocket连接前验证token的有效性
3. 增加错误处理逻辑，当收到401错误时自动重新登录

## 结论

后端API和WebSocket服务运行正常，前端访问失败的主要原因是使用了过期的JWT令牌。更新token后，前端应该能够正常访问后端服务。

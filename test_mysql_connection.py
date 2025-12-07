import pymysql

# 测试MySQL连接
try:
    # 使用用户提供的连接参数
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Dya20231108@',
        database='test',
        charset='utf8mb4'
    )
    print("连接成功！MySQL数据库连接参数正确。")
    conn.close()
except Exception as e:
    print(f"连接失败：{e}")
    print("请检查MySQL服务是否启动，以及用户名、密码、端口是否正确。")

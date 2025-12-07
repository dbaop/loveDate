from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# 创建数据库实例
db = SQLAlchemy()

# 导入所有模型，确保它们被SQLAlchemy识别
from app.models.user import User
from app.models.therapist import Therapist
from app.models.order import Order
from app.models.service import Service
from app.models.feedback import Feedback


def init_app(app: Flask):
    """初始化应用"""
    # 初始化数据库
    db.init_app(app)
    
    # 测试页面路由
    @app.route('/test')
    def test_page():
        return send_from_directory(app.static_folder, 'index.html')
    
    # 静态文件路由
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    # 创建表
    with app.app_context():
        db.create_all()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建数据库实例
db = SQLAlchemy()


def init_app(app: Flask):
    """初始化应用"""
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./aiyue_daojia.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 创建表
    with app.app_context():
        db.create_all()

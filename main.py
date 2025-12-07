import os
from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# 导入应用初始化函数
from app import init_app, db

# 导入蓝图
from app.api.user import user_bp
from app.api.therapist import therapist_bp
from app.api.order import order_bp
from app.api.service import service_bp
from app.api.feedback import feedback_bp
from app.api.message import message_bp
from app.api.websocket import socketio

# 导入配置
from config import config


def create_app(config_name=None):
    """创建并配置应用"""
    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'development'
    
    # 获取配置类
    config_class = config[config_name]
    app.config.from_object(config_class)
    
    # 初始化配置
    config_class.init_app(app)
    
    # 配置CORS
    if app.config['ENV'] == 'development':
        CORS(app, resources={"/*": {"origins": "*"}})  # 在开发环境允许所有跨域请求
    else:
        # 生产环境配置更严格的CORS
        CORS(app, 
             resources={"/*": {"origins": os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000')}}, 
             supports_credentials=True)
    
    # 初始化应用
    init_app(app)
    
    # 配置JWT
    jwt = JWTManager(app)
    
    # 配置数据库迁移
    migrate = Migrate(app, db)
    
    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(therapist_bp, url_prefix='/api/therapist')
    app.register_blueprint(order_bp, url_prefix='/api/order')
    app.register_blueprint(service_bp, url_prefix='/api/service')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(message_bp, url_prefix='/api/message')
    
    # 初始化SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # 健康检查端点
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'aiyue-daojia'}

    # 根路径
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    # 改回端口5000，适配前端配置
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

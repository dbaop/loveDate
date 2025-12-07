import os
import secrets
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler


class Config:
    """基础配置类"""
    # 应用基础配置
    APP_NAME = "LoveDate"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # 密钥配置 - 使用环境变量或生成安全随机密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(64)
    
    # 数据库基础配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_urlsafe(64)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)  # 访问令牌过期时间
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 刷新令牌过期时间
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    
    # 日志配置
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 其他基础配置
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 确保上传目录存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    ENV = 'development'
    
    # 开发环境数据库配置（SQLite）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///aiyue_daojia_dev.db'
    
    # 开发环境调试配置
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # 开发环境安全配置（放宽限制）
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    
    # 开发环境日志配置
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = os.path.join(Config.BASE_DIR, 'logs', 'app_dev.log')
    
    @staticmethod
    def init_app(app):
        """初始化开发环境配置"""
        Config.init_app(app)
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)
        
        # 配置日志
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(app.config['LOG_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
        
        # 添加日志处理器
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.info(f"{Config.APP_NAME} application started in development mode")


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    
    # 测试环境数据库配置（MySQL）
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(
            user=os.environ.get('DB_USER') or 'root',
            password=os.environ.get('DB_PASSWORD') or 'Dya20231108%40',
            host=os.environ.get('DB_HOST') or 'localhost',
            port=os.environ.get('DB_PORT') or '3306',
            db=os.environ.get('TEST_DB_NAME') or 'test'
        )
    
    # 测试环境特定配置
    WTF_CSRF_ENABLED = False  # 测试环境中禁用CSRF保护
    SQLALCHEMY_ECHO = True  # 打印SQL语句


class ProductionConfig(Config):
    """生产环境配置"""
    ENV = 'production'
    DEBUG = False
    
    # 生产环境数据库配置（MySQL）
    # 生产环境要求必须通过环境变量配置数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
    # 生产环境安全配置
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # 生产环境性能配置
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 60
    
    # 生产环境日志配置
    LOG_LEVEL = logging.ERROR
    LOG_FILE = os.path.join(Config.BASE_DIR, 'logs', 'app.log')
    
    @staticmethod
    def init_app(app):
        """初始化生产环境配置"""
        Config.init_app(app)
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)
        
        # 配置日志
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(app.config['LOG_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
        
        # 添加日志处理器
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.info(f"{Config.APP_NAME} application started in production mode")
        
        # 确保必须的环境变量已设置
        required_env_vars = ['DATABASE_URI', 'SECRET_KEY', 'JWT_SECRET_KEY']
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        if missing_vars:
            app.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")


# 配置映射，便于根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 获取当前环境配置
env_name = os.environ.get('FLASK_ENV') or 'development'
current_config = config[env_name]
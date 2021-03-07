import os


class Config:

    SERVICE_NAME = os.environ.get('SERVICE_NAME')
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    MONGO_URI = os.environ.get('MONGO_URI')
    if os.environ.get('LOG_PATH') is not None:
        LOG_PATH = os.environ.get('LOG_PATH')
    else:
        LOG_PATH = None


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'pre-production': ProductionConfig,
    'default': DevelopmentConfig
}

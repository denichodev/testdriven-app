class BaseConfig:
    """Base Configuration"""
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    pass


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    pass


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    pass

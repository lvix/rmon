import os

class DevConfig:
    """
    Development Config 
    """
    DEBUG = True 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True 

class ProductConfig(DevConfig):
    """
    Product Config 
    """
    DEBUG = False

    # path for sqlite db 
    path = os.path.join(os.getcwd(), 'rmon.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path)
    
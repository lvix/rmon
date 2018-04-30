""" rmon.app
"""

import os 
from flask import Flask 

from rmon.views import api 
from rmon.models import db 
from rmon.config import  DevConfig, ProductConfig 

def create_app():
    """create and initialize app 
    """

    app = Flask('rmon')

    env = os.environ.get('RMON_ENV')

    if env in ('pro', 'prod', 'proudct'):
        app.config.from_object(ProductConfig)
    else:
        app.config.from_object(DevConfig)

    app.config.from_envvar('RMON_SETTTINGS', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    app.register_blueprint(api)

    db.init_app(app)

    if app.debug:
        with app.app_context():
            db.create_all()

    return app
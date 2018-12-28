from flask import Flask

from app.house import house_bp
from app.models import db
from app.orders import order_bp
from app.user import user_bp
from utils.config import Conf
from utils.settings import TEMPLATES_PATH, STATIC_PATH


def create_app():
    app = Flask(__name__,
                static_folder=STATIC_PATH,
                template_folder=TEMPLATES_PATH,)

    app.config.from_object(Conf)
    db.init_app(app)
    app.register_blueprint(blueprint=user_bp, url_prefix='/user')
    app.register_blueprint(blueprint=house_bp, url_prefix='/house')
    app.register_blueprint(blueprint=order_bp, url_prefix='/order')
    return app

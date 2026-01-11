from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)

    # Регистрация блюпринтов (маршрутов)
    from .routes import main
    app.register_blueprint(main)

    # Создание таблиц БД при запуске, если их нет
    with app.app_context():
        db.create_all()

    return app
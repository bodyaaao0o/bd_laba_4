import os
import secrets
from typing import Dict, Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

# Константи для налаштувань
SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

# Ініціалізація SQLAlchemy
db = SQLAlchemy()

# Тимчасове зберігання для даних todos
todos = {}

from back_flask_bd.app.my_project.auth.route.orders.user_route import user_bp


def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config.update(app_config)

    # Реєстрація `Blueprint`
    app.register_blueprint(user_bp)

    print("User blueprint registered successfully!")
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule}, Endpoint: {rule.endpoint}")

    _init_db(app)

    @app.route('/')
    def hello():
        return "Hello World!"

    return app


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    root_user = os.getenv(MYSQL_ROOT_USER, additional_config.get(MYSQL_ROOT_USER))
    root_password = os.getenv(MYSQL_ROOT_PASSWORD, additional_config.get(MYSQL_ROOT_PASSWORD))

    # Форматуємо SQLALCHEMY_DATABASE_URI з позиційними параметрами
    if SQLALCHEMY_DATABASE_URI in app_config:
        app_config[SQLALCHEMY_DATABASE_URI] = app_config[SQLALCHEMY_DATABASE_URI].format(
            root_user, root_password
        )
    else:
        raise ValueError("SQLALCHEMY_DATABASE_URI must be provided in app_config.")



def _init_db(app: Flask) -> None:
    """
    Ініціалізує базу даних для Flask-додатку.
    """
    db.init_app(app)

    # Перевіряємо, чи існує база даних; якщо ні — створюємо її
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if db_uri and not database_exists(db_uri):
        create_database(db_uri)

    # Імпорт ваших моделей
    import back_flask_bd.app.my_project.auth.domain

    # Створюємо всі таблиці в базі даних
    with app.app_context():
        db.create_all()

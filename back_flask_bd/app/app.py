import os
from waitress import serve
import yaml
from back_flask_bd.app.my_project import create_app

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"


if __name__ == '__main__':
    # Отримуємо середовище (розробка або продакшн)
    flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()
    config_yaml_path = os.path.join(os.getcwd(), 'config', 'app.yml')

    # Завантажуємо конфігураційні дані з YAML файлу
    with open(config_yaml_path, 'r', encoding='utf-8') as yaml_file:
        config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
        additional_config = config_data_dict[ADDITIONAL_CONFIG]

        # Вибір конфігурації в залежності від середовища
        if flask_env == DEVELOPMENT:
            config_data = config_data_dict[DEVELOPMENT]
            # Створюємо додаток і запускаємо його в режимі розробки
            create_app(config_data, additional_config).run(port=DEVELOPMENT_PORT, debug=True)

        elif flask_env == PRODUCTION:
            config_data = config_data_dict[PRODUCTION]
            # Створюємо додаток і запускаємо його через waitress для продакшн середовища
            serve(create_app(config_data, additional_config), host=HOST, port=PRODUCTION_PORT)

        else:
            raise ValueError("flask_env must be either 'development' or 'production'")

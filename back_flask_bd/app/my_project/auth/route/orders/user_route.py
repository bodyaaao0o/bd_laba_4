from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response
from back_flask_bd.app.my_project.auth.controller import user_controller
from back_flask_bd.app.my_project.auth.domain import User

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET'])
def get_all_users() -> Response:
    user_controller_instance = user_controller()
    return make_response(jsonify(user_controller_instance.find_all()), HTTPStatus.OK)


@user_bp.post('/')
def create_user() -> Response:
    content = request.get_json()

    # Створіть об'єкт моделі User безпосередньо з отриманого контенту
    user = User.create_user(content)  # Припустимо, що create_user повертає екземпляр User

    # Тепер передайте екземпляр моделі до контролера
    user_controller_instance = user_controller()
    user_controller_instance.create(user)  # Передайте об'єкт моделі, а не словник

    return make_response(jsonify(user.put_into_dto()), HTTPStatus.CREATED)



@user_bp.get('/<int:user_id>')
def get_user(user_id: int) -> Response:
    user_controller_instance = user_controller()
    return make_response(jsonify(user_controller_instance.find_by_id(user_id)), HTTPStatus.OK)


@user_bp.put('/<int:user_id>')
def update_user(user_id: int) -> Response:
    content = request.get_json()

    if content is None:
        abort(HTTPStatus.BAD_REQUEST, "No data provided")

    # Переконайтеся, що ви створюєте об'єкт правильно
    user = User.create_from_dto(content)  # Переконайтеся, що метод create_from_dto правильно працює

    user_controller_instance = user_controller()
    user_controller_instance.update(user_id, user)  # Передайте екземпляр моделі

    return make_response("User  updated", HTTPStatus.OK)


@user_bp.patch('/<int:user_id>')
def patch_user(user_id: int) -> Response:
    content = request.get_json()
    user_controller.patch(user_id, content)
    return make_response("User updated", HTTPStatus.OK)

@user_bp.delete('/<int:user_id>')
def delete_user(user_id: int) -> Response:
    user_controller_instance = user_controller()
    user_controller_instance.delete(user_id)
    return make_response("User deleted", HTTPStatus.OK)
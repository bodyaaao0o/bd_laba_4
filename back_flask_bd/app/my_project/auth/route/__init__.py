from flask import Flask

from .error_handler import err_handler_bp

def register_routes(app: Flask) -> None:
    app.register_blueprint(err_handler_bp)

    from .orders.user_route import user_bp

    app.register_blueprint(user_bp)
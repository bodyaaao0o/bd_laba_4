from __future__ import annotations
from typing import Dict, Any


from flask_sqlalchemy import SQLAlchemy
from back_flask_bd.app.my_project.auth.domain.i_dto import IDto

db = SQLAlchemy()

class User(db.Model, IDto):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    chats = db.relationship('ChatParticipant', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.id}, {self.username}', '{self.email}', '{self.password}')"

    def put_into_dto(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def create_user(dto_dict: Dict[str, Any]) -> User:

        obj = User(**dto_dict)
        return obj

    @classmethod
    def create_from_dto(cls, dto):
        # Переконайтеся, що ви передаєте всі необхідні дані
        if 'username' not in dto or 'email' not in dto:
            return None  # або підніміть виключення, якщо дані неповні

        return cls(**dto)
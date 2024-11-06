from abc import ABC
from typing import List

from sqlalchemy import inspect
from sqlalchemy.orm import Mapper

from back_flask_bd.app.my_project import db


class GeneralDao(ABC):
    _domain_type = None
    _session = db.session


    def find_all(self):
        return self._session.query(self._domain_type).all()

    def find_by_id(self, key: int) -> object:

        return self._session.query(self._domain_type).get(key)

    def create(self, obj: object) -> object:

        self._session.add(obj)
        self._session.commit()
        return obj

    def create_all(self, objs: List[object]) -> List[object]:
        self._session.add_all(objs)
        self._session.commit()
        return objs

    def update(self,key: int, in_obj: object) -> object:

        domain_obj = self._session.query(self._domain_type).get(key)
        mapper: Mapper = inspect(type(in_obj))
        columns = mapper.columns._collection
        for colomn_name, colomn_obj, *_ in columns:
            if not colomn_obj.primary_key:
                value = getattr(in_obj, colomn_name)
                setattr(in_obj, colomn_name, value)
        self._session.commit()

    def patch(self, key: int, field_name: str, value: object) -> None:
        domain_obj = self._session.query(self._domain_type).get(key)
        setattr(domain_obj, field_name, value)  # Заміна значення поля
        self._session.commit()


    def delete(self, key: int) -> None:
        domain_obj = self._session.query(self._domain_type).get(key)
        self._session.delete(domain_obj)
        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def delete_all(self) -> None:

        self._session.query(self._domain_type).delete()
        self._session.commit()

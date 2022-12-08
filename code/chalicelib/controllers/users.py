from dataclasses import dataclass
from typing import Dict, List, Text, Any

import bcrypt
from chalice import NotFoundError
from pymongo.collection import Mapping

from chalicelib import HTTPMethod
from chalicelib.controllers import BaseController
from chalicelib.database.collections import User
from chalicelib.utils import get_object_id, StandardResponse


class SecurityController:
    @classmethod
    def generate_password_hash(cls, password: Text) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @classmethod
    def check_user_credentials(cls, username: str, password: str) -> Mapping[str, Any]:
        user = User.find_one({'username': username})
        if not user:
            raise NotFoundError('User not found')
        check_user = bcrypt.checkpw(password.encode('utf-8'), hashed_password=user['password'])
        if not check_user:
            raise NotFoundError('Invalid password')
        return user


@dataclass
class UserController(BaseController):

    def __load_data(self) -> Dict:
        self._validate_data()
        return self.schema_class().load(self.body_dict)

    def _get_users(self) -> Dict:
        users_q = User.find()
        return self.schema_class(many=True).dump(users_q)

    def _create_user(self) -> Dict:
        user_data = self.__load_data()
        user_data['password'] = SecurityController.generate_password_hash(user_data['password'])
        user = User.insert_one(user_data)
        get_user = User.find_one({'_id': user.inserted_id})
        return self.schema_class().dump(get_user)

    def __call__(self, *args, **kwargs) -> List[Dict] or Dict:
        data, message, status_code = {}, '', 200
        if self.http_method == HTTPMethod.GET.value:
            data = self._get_users()
            message = 'Users retrieved successfully'
        elif self.http_method == HTTPMethod.POST.value:
            data = self._create_user()
            message = 'User created successfully'
            status_code = 201
        return StandardResponse(message=message, data=data, status_code=status_code)()


@dataclass
class RetrieveUserController(BaseController):

    def __load_data(self, partial: bool = False) -> Dict:
        if not partial:
            self._validate_data()
        return self.schema_class(
            exclude=('password',) if self.http_method != HTTPMethod.POST.value else ()
        ).load(
            data=self.body_dict,
            partial=partial
        )

    def _get_user(self):
        object_id = get_object_id(self.id_field)
        return User.find_one({'_id': object_id})

    def _update_user(self):
        object_id = get_object_id(self.id_field)
        return User.find_one_and_update(
            {'_id': object_id},
            {'$set': self.__load_data(partial=True)},
            return_document=True,
        )

    def _delete_user(self):
        object_id = get_object_id(self.id_field)
        return User.find_one_and_delete({'_id': object_id})

    def __call__(self):
        data, message, status_code = {}, '', 200
        if self.http_method == HTTPMethod.GET.value:
            data = self.schema_class().dump(self._get_user())
            message = 'User retrieved successfully'
        elif self.http_method == HTTPMethod.PUT.value:
            data = self.schema_class().dump(self._update_user())
            message = 'User updated successfully'
        elif self.http_method == HTTPMethod.DELETE.value:
            data = self.schema_class().dump(self._delete_user())
            message = 'User deleted successfully'
            status_code = 204
        return StandardResponse(data=data, message=message, status_code=status_code)()

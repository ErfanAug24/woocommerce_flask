from werkzeug.security import check_password_hash, generate_password_hash
from src.api_v2.models.user import UserModel
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jti)
from flask_restful import Resource, reqparse
from src.api_v2.models.blacklist import User_BlackList

_user_parsar = reqparse.RequestParser()
_user_parsar.add_argument('username', type=str,
                          required=True,
                          help='this field is required')
_user_parsar.add_argument('email', type=str,
                          required=True,
                          help='this field is required')
_user_parsar.add_argument('password', type=str,
                          required=True,
                          help='this field is required')


class User_API(Resource):

    def get(self, username: str):
        user = UserModel.find_by_username(username)
        return user.json() if user else {'message': 'store not found !'}, 404

    def post(self, username: str):
        user = UserModel.find_by_username(username)
        if user:
            return {'message': 'this user is already exist !'}, 400
        data = _user_parsar.parse_args()
        user = UserModel(username, data.get('email'), generate_password_hash(data.get('password')))
        user.save_to_db()
        return user.json(), 201

    @jwt_required()
    def delete(self, username: str):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return user.json()
        return {'message': 'store not found !'}, 404

    def put(self, username):
        pass


class UserList(Resource):

    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        """
        get data from parser
        find user in database
        check password
        create access token
        create refresh token
        :return: them
        """
        data = _user_parsar.parse_args()
        user = UserModel.find_by_username(data.get('username'))
        if user and check_password_hash(user.password, data.get('password')):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jti()
        jti.save_to_db()
        return {'message': 'successfully logged out'}

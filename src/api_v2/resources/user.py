from werkzeug.security import check_password_hash, generate_password_hash
from src.api_v2.models.user import UserModel
from src.api_v2.models.blacklist import User_BlackList
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt,
                                get_jwt_identity)
from flask_restful import Resource, reqparse

BLACK_ERROR = 'this user field {} is required'
ITEM_NOT_FOUND = 'user not found !'
REGISTERED_ITEM = 'This user is already in database'
ITEM_DELETED = 'user has been deleted!'

_user_parsar = reqparse.RequestParser()
_user_parsar.add_argument('username', type=str,
                          required=True,
                          help=BLACK_ERROR.format('username'))
_user_parsar.add_argument('email', type=str,
                          required=True,
                          help=BLACK_ERROR.format('email'))
_user_parsar.add_argument('password', type=str,
                          required=True,
                          help=BLACK_ERROR.format('password'))


class User_API(Resource):
    @classmethod
    @jwt_required()
    def get(cls, username: str):
        user = UserModel.find_by_username(username)
        return user.json() if user else {'message': ITEM_NOT_FOUND}, 404

    # @jwt_required(fresh=True)
    @classmethod
    def post(cls, username: str):
        user = UserModel.find_by_username(username)
        if user:
            return {'message': REGISTERED_ITEM}, 400
        data = _user_parsar.parse_args()
        user = UserModel(username, data.get('email'), generate_password_hash(data.get('password')))
        user.save_to_db()
        return user.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, username: str):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return user.json()
        return {'message': ITEM_DELETED}, 404

    @classmethod
    def put(cls, username):
        pass


class UserList(Resource):
    @classmethod
    def get(cls):
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
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        jti = get_jwt()["jti"]
        token_in_blacklist = User_BlackList(jti, "Expired Token Due To logging out!")
        token_in_blacklist.save_to_db()
        return {'message': 'successfully logged out'}

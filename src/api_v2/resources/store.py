from flask_restful import Resource, reqparse
from src.api_v2.models.store import StoreModel

STORE_ALREADY_EXIST = "A store with name {} is already exist !"
NOT_FOUND = 'Store not found!'
DELETE_STORE = 'the store with name {} has been deleted!'
BLACK_ERROR = 'this store field {} is required'

_store_parser = reqparse.RequestParser()
_store_parser.add_argument('name', type=str,
                           required=True,
                           help=BLACK_ERROR.format('name'))
_store_parser.add_argument('price', type=str,
                           required=True,
                           help=BLACK_ERROR.format('price'))
_store_parser.add_argument('user_id', type=str,
                           required=True,
                           help=BLACK_ERROR.format('user_id'))


class Store_API(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        return store.json(), 200 if store else {'message': NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.quantity += 1
            store.save_to_db()
            return store.json()
        data = _store_parser.parse_args()
        store = StoreModel(name, data.get('price'), data.get('user_id'))
        store.save_to_db()
        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': DELETE_STORE.format(name)}, 200
        return {'message': NOT_FOUND}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}

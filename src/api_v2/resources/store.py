from flask_restful import Resource, reqparse
from src.api_v2.models.store import StoreModel


class Store_API(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str,
                        required=True,
                        help='this field is required to be.')
    parser.add_argument('price', type=str,
                        required=True,
                        help='this field is required to be.')
    parser.add_argument('user_id', type=str,
                        required=True,
                        help='for each store you need an user_id')

    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        return store.json() if store else {'message': 'store not found !'}, 404

    def post(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.quantity += 1
            store.save_to_db()
            return store.json()
        data = Store_API.parser.parse_args()
        store = StoreModel(name, data.get('price'), data.get('user_id'))
        store.save_to_db()
        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'the store deleted !'}, 200
        return {'message': 'store not found !'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}

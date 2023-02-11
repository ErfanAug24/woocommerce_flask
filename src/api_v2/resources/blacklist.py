from flask_restful import Resource, reqparse
from src.api_v2.models.blacklist import User_BlackList


class BlackList_Request(Resource):
    @classmethod
    def get(cls):
        return {'blacklist_tokens': list(map(lambda x: x.json(), User_BlackList.query.all()))}

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from src.api_v2.resources.user import User_API, UserList, UserLogin, TokenRefresh, UserLogout
from src.api_v2.resources.store import Store_API, StoreList
from src.api_v2.models.blacklist import User_BlackList
from src.api_v2.resources.blacklist import BlackList_Request


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # registering database

    from src.db import db
    db.init_app(app)

    # adding apis to resources
    api = Api(app)

    # creating jwt
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_blacklist = User_BlackList.find_by_jwt_id(jti)
        return token_in_blacklist is not None

    # adding api to resource

    api.add_resource(User_API, '/user/<string:username>')
    api.add_resource(UserList, '/users')
    api.add_resource(Store_API, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(BlackList_Request, '/blacklist')

    # adding blueprints
    from src.Front_End_Api.Base_api.routes import base_header_urls
    from src.Front_End_Api.Store_api.routes import store_url
    app.register_blueprint(base_header_urls)
    app.register_blueprint(store_url)

    # registering marshmallow
    from src.api_v2.models.db_auth import ma
    ma.init_app(app)

    return app

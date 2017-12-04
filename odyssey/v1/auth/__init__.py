from flask import Blueprint
from flask_restful import Api
from odyssey.v1.form.controllers.form_api import RegisterAPI
from odyssey.v1.auth.controllers.auth_api import AuthAPI

auth_blueprint_v1 = Blueprint('auth_blueprint_v1', __name__)
api = Api(auth_blueprint_v1, prefix='/api/v1/auth')

api.add_resource(AuthAPI, '/<string:auth_function>', strict_slashes=False)


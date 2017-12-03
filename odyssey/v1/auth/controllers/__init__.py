from flask import Blueprint
from flask_restful import Api
from odyssey.v1.auth.customer_errors import errors

register_blueprint = Blueprint('auth_blueprint_v1', __name__)
api = Api(register_blueprint, prefix='/api/v2/auth', errors=errors)

api.add_resource(RegisterAPI, 'register', strict_slashes=False)


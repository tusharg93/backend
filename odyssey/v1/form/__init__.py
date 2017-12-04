from flask import Blueprint
from flask_restful import Api
from odyssey.v1.form.customer_errors import errors
from odyssey.v1.form.controllers.form_api import RegisterAPI
from odyssey.v1.form.controllers.email_verify_api import EmailVerifyAPI

register_blueprint_v1 = Blueprint('register_blueprint_v1', __name__)
api = Api(register_blueprint_v1, prefix='/api/v1/forms', errors=errors)

api.add_resource(RegisterAPI, '/register', strict_slashes=False)
api.add_resource(EmailVerifyAPI,'/verify-email',strict_slashes=False)


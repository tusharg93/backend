from flask import Blueprint
from flask_restful import Api
from odyssey.v1.form.controllers.form_api import RegisterAPI
from odyssey.v1.form.controllers.email_verify_api import EmailVerifyAPI
from odyssey.v1.form.controllers.default_api import DefaultAPI
from odyssey.v1.form.controllers.fill_sections_api import FillSectionsAPI

register_blueprint_v1 = Blueprint('register_blueprint_v1', __name__)
api = Api(register_blueprint_v1, prefix='/api/v1/forms')

api.add_resource(RegisterAPI, '/register', strict_slashes=False)
api.add_resource(EmailVerifyAPI,'/verify-email',strict_slashes=False)
api.add_resource(DefaultAPI,'/defaults',strict_slashes=False)
api.add_resource(FillSectionsAPI, '/<string:section>', strict_slashes=False)

from flask import Blueprint
from flask_restful import Api
from odyssey.v1.form.controllers.form_api import RegisterAPI
from odyssey.v1.form.controllers.email_verify_api import EmailVerifyAPI
from odyssey.v1.form.controllers.default_api import DefaultAPI
from odyssey.v1.form.controllers.fill_sections_api import FillSectionsAPI
from odyssey.v1.form.controllers.image_upload_api import ImageUploadAPI
from odyssey.v1.form.controllers.gc_profile_api import GCProfileAPI
from odyssey.v1.form.controllers.dashboard_api import DashBoardAPI
from odyssey.v1.form.controllers.contract_request_api import ContractRequestAPI

forms_blueprint_v1 = Blueprint('forms_blueprint_v1', __name__)
api = Api(forms_blueprint_v1, prefix='/api/v1/forms')

api.add_resource(RegisterAPI, '/register', strict_slashes=False)
api.add_resource(EmailVerifyAPI,'/verify-email',strict_slashes=False)
api.add_resource(DefaultAPI,'/defaults',strict_slashes=False)
api.add_resource(FillSectionsAPI, '/<string:section>', strict_slashes=False)
api.add_resource(ImageUploadAPI,'/image',strict_slashes=False)
api.add_resource(GCProfileAPI,'/profile',strict_slashes=False)
api.add_resource(DashBoardAPI,'/dashboard',strict_slashes=False)
api.add_resource(ContractRequestAPI,'/request',strict_slashes=False)
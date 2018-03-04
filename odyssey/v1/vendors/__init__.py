from flask import Blueprint
from flask_restful import Api
from odyssey.v1.vendors.controllers.vendor_profile_api import VendorProfileAPI
from odyssey.v1.vendors.controllers.register_api import VendorRegisterAPI
from odyssey.v1.vendors.controllers.image_upload_api import ImageUploadAPI
from odyssey.v1.vendors.controllers.dashboard_api import VendorDashboardAPI
from odyssey.v1.vendors.controllers.request_contract_api import RequestContract

vendors_blueprint_v1 = Blueprint('vendors_blueprint_v1', __name__)
api = Api(vendors_blueprint_v1, prefix='/api/v1/vendors')

api.add_resource(VendorProfileAPI, '/profile', strict_slashes=False)
api.add_resource(VendorRegisterAPI,'/register',strict_slashes=False)
api.add_resource(ImageUploadAPI,'/image',strict_slashes=False)
api.add_resource(VendorDashboardAPI,'/dashboard',strict_slashes=False)
api.add_resource(RequestContract,'/request',strict_slashes=False)

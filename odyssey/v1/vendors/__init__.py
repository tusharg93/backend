from flask import Blueprint
from flask_restful import Api
from odyssey.v1.vendors.controllers.vendor_profile_api import VendorProfileAPI
from odyssey.v1.vendors.controllers.register_api import VendorRegisterAPI

vendors_blueprint_v1 = Blueprint('vendors_blueprint_v1', __name__)
api = Api(vendors_blueprint_v1, prefix='/api/v1/vendors')

api.add_resource(VendorProfileAPI, '/profile', strict_slashes=False)
api.add_resource(VendorRegisterAPI,'/register',strict_slashes=False)
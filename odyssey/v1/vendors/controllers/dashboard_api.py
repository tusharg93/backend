from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.vendors.functions import load_home_page_data
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.auth.login_decorators import login_required
from flask import g, request

class VendorDashboardAPI(Resource):
    method_decorators = [login_required]
    def get(self):
        try:
            user_id = g.user.id
            data = load_home_page_data(user_id)
            return {"status": OK, "data":data},OK
        except:
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

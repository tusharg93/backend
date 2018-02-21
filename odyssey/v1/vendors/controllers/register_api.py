from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.vendors.functions import register_vendor_data
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from flask import request
from odyssey import app

class VendorRegisterAPI(Resource):

    def post(self):
        try:
            register_vendor_data(request.json)
            return {"status": CREATED, "msg": "success"},CREATED
        except Exception,e:
            import traceback
            app.logger.info("Error in reigster api {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK

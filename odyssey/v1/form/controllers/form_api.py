from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.form.functions import register_form_data
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from flask import request
from odyssey.v1.form.customer_errors import UserExistsException
from odyssey import app

class RegisterAPI(Resource):

    def post(self):
        try:
            register_form_data(request.json)
            return {"status": CREATED, "msg": "success"},CREATED
        except UserExistsException:
            return {"status":INTERNAL_SERVER_ERROR, "msg":"failure","error":"email already exists"},OK
        except Exception,e:
            import traceback
            app.logger.info("Error in reigster api {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

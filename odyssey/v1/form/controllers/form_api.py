from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.form.functions import register_form_data
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.status_messages import MSG_OK, INTERNAL_ERROR
from flask import request


class RegisterAPI(Resource):

    def post(self):
        try:
            register_form_data(request.json)
            return {"status": MSG_OK, "msg": "success"},CREATED
        except Exception,e:

            return {"status": INTERNAL_ERROR, "msg": "failure","error":str(e)},INTERNAL_SERVER_ERROR

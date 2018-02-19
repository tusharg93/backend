from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.form.functions import verify_email
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.status_messages import MSG_OK, INTERNAL_ERROR
from flask import request


class EmailVerifyAPI(Resource):

    def get(self):
        try:
            result    =   verify_email(request.args)
            if result:
                return {"status": MSG_OK, "msg": "success"},OK
            else:
                return {"status":UNAUTHORIZED,"msg":"failure"},OK
        except Exception, e:
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK

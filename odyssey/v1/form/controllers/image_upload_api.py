from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.form.functions import image_upload
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.status_messages import MSG_OK, INTERNAL_ERROR
from odyssey.v1.auth.login_decorators import login_required
from flask import g, request

class ImageUploadAPI(Resource):
    method_decorators = [login_required]
    def post(self):
        try:
            user_id = g.user.id
            image_upload(user_id, request)
            return {"status": OK, "msg": "success"},OK
        except Exception, e:
            return {"status": INTERNAL_ERROR, "msg": "failure"},OK

    def put(self):
        try:
            user_id = g.user.id
            image_upload(user_id, request)
            return {"status": OK, "msg": "success"},OK
        except Exception, e:
            return {"status": INTERNAL_ERROR, "msg": "failure"},OK
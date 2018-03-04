from flask_restful import Resource
from flask import g
from odyssey.v1.auth.login_decorators import login_required
from odyssey.v1.vendors.functions import course_request
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from flask import request
from odyssey import app

class RequestContract(Resource):
    method_decorators = [login_required]
    def post(self):
        try:
            user_id = g.user.id
            course_request(user_id, request.json)
            return {"status": OK, "msg": "success"},OK
        except:
            import traceback
            app.logger.info("Error in vendor contract request api {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

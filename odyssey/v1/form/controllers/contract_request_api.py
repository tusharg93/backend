from flask_restful import Resource
from flask import g
from odyssey.v1.auth.login_decorators import login_required
from odyssey.v1.form.functions import vendor_request
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from flask import request
from odyssey import app

class ContractRequestAPI(Resource):
    method_decorators = [login_required]
    def post(self):
        try:
            user_id = g.user.id
            vendor_request(user_id, request.json)
            return {"status": OK, "msg": "success"},OK
        except:
            import traceback
            app.logger.info("Error in course contract api {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

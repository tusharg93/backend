from flask_restful import Resource
from odyssey.v1.common.functions import get_default_values
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.auth.login_decorators import login_required

class DefaultAPI(Resource):
    method_decorators = [login_required]
    def get(self):
        try:
            result    =   get_default_values()
            return {"status": OK, "msg": "success", "data":result},OK
        except Exception, e:
            import traceback
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

from flask_restful import Resource
from odyssey.v1.status_codes import *
from odyssey.v1.common.functions import get_default_values
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.status_messages import MSG_OK, INTERNAL_ERROR


class DefaultAPI(Resource):

    def get(self):
        try:
            result    =   get_default_values()
            return {"status": MSG_OK, "msg": "success", "data":result},OK
        except Exception, e:
            return {"status": INTERNAL_ERROR, "msg": "failure","error":str(e)},OK

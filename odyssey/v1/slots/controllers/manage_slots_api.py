from flask_restful import Resource
from flask import g
from odyssey.v1.slots.functions import get_week_type_slots,get_date_wise_slot,update_date_wise_slot,update_week_type_slots
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR,BAD_REQUEST
from odyssey.v1.auth.login_decorators import login_required
from flask import request
from odyssey import app

class ManageSlotsAPI(Resource):
    method_decorators = [login_required]
    def get(self):
        try:
            gc_id = g.user.id
            filter_type = request.args.get("type")
            result = list()
            if filter_type == "seasons":
                result = get_week_type_slots(gc_id, request.args)
            elif filter_type == "date":
                result = get_date_wise_slot(gc_id, request.args)
            else:
                return {"status":BAD_REQUEST,"msg":"failure"},OK
            return {"status": OK, "msg": "success", "data": result}, OK
        except Exception,e:
            import traceback
            app.logger.info("Error in filter get slots {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK


    def put(self):
        try:
            gc_id = g.user.id
            filter_type = request.json.get('type')
            if filter_type == "seasons":
                update_week_type_slots(gc_id, request.json)
            elif filter_type == "date":
                update_date_wise_slot(gc_id, request.json)
            else:
                return {"status": BAD_REQUEST, "msg": "failure"}, OK
            return {"status":OK,"msg":"success"},OK

        except Exception,e:
            import traceback
            app.logger.info("Error in filter update slots {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK

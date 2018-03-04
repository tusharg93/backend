from flask_restful import Resource
from flask import g
from odyssey.v1.slots.functions import update_closed_days, update_holiday_days, create_closed_days, create_holiday_days
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.auth.login_decorators import login_required
from flask import request
from odyssey import app

class ManageDaysAPI(Resource):
    method_decorators = [login_required]

    def post(self):
        try:
            gc_id = g.user.id
            days_type = request.json.get('type')
            if days_type == "closed":
                create_closed_days(gc_id, request.json)
            elif days_type == "holiday":
                create_holiday_days(gc_id, request.json)
            return {"status":OK,"msg":"success"},OK
        except Exception,e:
            import traceback
            app.logger.info("Error in filter create slots {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK

    def put(self):
        try:
            gc_id = g.user.id
            days_type = request.json.get('type')
            if days_type == "closed":
                update_closed_days(gc_id, request.json)
            elif days_type == "holiday":
                update_holiday_days(gc_id, request.json)
            return {"status":OK,"msg":"success"},OK
        except Exception,e:
            import traceback
            app.logger.info("Error in filter update slots {}".format(traceback.print_exc()))
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure","error":str(e)},OK

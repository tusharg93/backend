from flask_restful import Resource
from flask import g
from odyssey import app
from odyssey.v1.form.functions import load_home_page_data
from odyssey.v1.status_codes import OK,INTERNAL_SERVER_ERROR
from odyssey.v1.auth.login_decorators import login_required

class DashBoardAPI(Resource):
    method_decorators = [login_required]
    def get(self):
        try:
            user_id   =   g.user.id
            result    =   load_home_page_data(user_id)
            return {"status": OK, "msg": "success", "data":result},OK
        except:
            import traceback
            app.logger.info("error in dashboard golf course api")
            app.logger.error(traceback.print_exc())
            return {"status": INTERNAL_SERVER_ERROR, "msg": "failure"},OK

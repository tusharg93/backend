from flask_restful import Resource
from flask import g, request
from odyssey.v1.auth.exceptions import *
from odyssey.v1.form.functions import *
from odyssey.v1.auth.login_decorators import login_required
from odyssey.v1.status_codes import *
from odyssey import app, db


class FillSectionsAPI(Resource):
    method_decorators = [login_required]
    def post(self, section):
        try:
            if g and g.user:
                gc_id = g.user.id
            else:
                gc_id = None
            app.logger.info("Login id {}".format(gc_id))
            if section == '1':
                gc_fill_section_1(request.json, gc_id)
            elif section == '2':
                gc_fill__section_2(request.json,gc_id)
            elif section == '3':
                gc_fill_section_3(request.json,gc_id)
            elif section == '4':
                gc_fill_section_4(request.json,gc_id)
            else:
                return {"status":BAD_REQUEST,"msg":"failure"},OK
            return {"status":OK,"msg":"success"},OK
        except:
            import traceback
            db.session.rollback()
            app.logger.error('Unknown Error in login'.format(str(traceback.print_exc())))
            return {"status":INTERNAL_SERVER_ERROR, "error": "some error occured"}, OK


from flask_restful import Resource
from odyssey.v1.auth.exceptions import *
from odyssey.v1.auth.functions import process_auth
from odyssey.v1.status_codes import *
from odyssey import app


class AuthAPI(Resource):
    def post(self, auth_function):
        try:

            response = process_auth(auth_function)
            return {
                       'status': 'OK',
                       'data': response
                   } if response else {
                'status': 'OK'
            }, OK

        except BadRequestException:
            return {"status":BAD_REQUEST,"error": "invalid request"}, BAD_REQUEST

        except UserNotFoundException:
            return {"status":NOT_FOUND,"error": "user not found"}, OK

        except UserWrongPasswordException:
            return {"status":UNAUTHORIZED,"error": "invalid login details"}, UNAUTHORIZED

        except EmailNotVerifiedException:
            return {"status":UNAUTHORIZED, "error": "email not verified"}, UNAUTHORIZED

        except:
            import traceback
            app.logger.error('Unknown Error in login'.format(str(traceback.print_exc())))
            return {"status":INTERNAL_SERVER_ERROR, "error": "some error occured"}, OK


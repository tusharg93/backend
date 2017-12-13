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
            return {"error": "invalid request"}, BAD_REQUEST

        except UserNotFoundException:
            return {"error": "user not found"}, NOT_FOUND

        except UserWrongPasswordException:
            return {"error": "invalid login details"}, UNAUTHORIZED

        except EmailNotVerifiedException:
            return {"error": "email not verified"}, UNAUTHORIZED

        except:
            import traceback
            app.logger.error('Unknown Error in login'.format(str(traceback.print_exc())))
            return {"error": "some error occured"}, INTERNAL_SERVER_ERROR


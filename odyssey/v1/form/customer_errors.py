from flask_restful import HTTPException


class UserExistsException(HTTPException):
    pass

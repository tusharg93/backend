from flask_restful import HTTPException


class UserNotFoundException(HTTPException):
    pass


class UserWrongPasswordException(HTTPException):
    pass

class EmailNotVerifiedException(HTTPException):
    pass

class OTPLoginIDNullException(HTTPException):
    pass


class OTPSelfNullException(HTTPException):
    pass


class OTPAuthTokenNullException(HTTPException):
    pass


class WrongAuthTokenException(HTTPException):
    pass


class WrongOTPException(HTTPException):
    pass


class ResetPasswordNullException(HTTPException):
    pass


class BadRequestException(HTTPException):
    pass


class OrganizationNotFoundException(HTTPException):
    pass


class UserNotAgentException(HTTPException):
    pass


class UserNotManagerException(HTTPException):
    pass

class InternalServerError(HTTPException):
    pass

class ServiceNotEnabled(HTTPException):
    pass
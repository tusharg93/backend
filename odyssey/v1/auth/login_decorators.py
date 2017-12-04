from functools import wraps

from flask import g, session
from odyssey import app

from odyssey.v1.common.functions import \
    unauthorized_view

def login_required(callback):
    """
    This decorator ensures that the current user has logged in before proceeding.
    Calls the unauthorized_view() when requirements fail.
    :param callback: callback function
    :return: callback function if successful else unauthorized.
    """

    @wraps(callback)
    def wrapper(*args, **kwargs):
        # app.logger.warn("LOGIN WRAPPER. USER: {}. SESSION: {}".format(
        #     g.user.id if g.user else "NULL",
        #     session['user_id'] if 'user_id' in session else "NULL"
        # ))
        if not (g.user and g.user.is_authenticated):
            # app.logger.warn("LOGIN WRAPPER. UNAUTHENTICATED: {}".format(session['user_id'] if 'user_id' in session else "NULL"))
            return unauthorized_view()
        return callback(*args, **kwargs)

    return wrapper


# def roles_required(*role_names):
#     """
#     This decorator ensures that the current user has all of the specified roles.
#     Calls the unauthorized_view() when requirements fail.
#     :param role_names:
#     :return:
#     """
#     def wrapper(function):
#         @wraps(function)
#         def decorated_view(*args, **kwargs):
#             if not (g.user and g.user.is_authenticated):
#                 return unauthorized_view()
#             if not is_authorized(g.user, role_names):
#                 return unauthorized_view()
#             return function(*args, **kwargs)
#
#         return decorated_view
#
#     return wrapper
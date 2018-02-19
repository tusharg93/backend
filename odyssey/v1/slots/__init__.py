from flask import Blueprint
from flask_restful import Api
from odyssey.v1.slots.controllers.manage_slots_api import ManageSlotsAPI

slots_blueprint_v1 = Blueprint('slots_blueprint_v1', __name__)
api = Api(slots_blueprint_v1, prefix='/api/v1/slots')

api.add_resource(ManageSlotsAPI, '/filter', strict_slashes=False)

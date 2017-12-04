# -*- coding: utf-8 -*-

from flask import g, request, abort, make_response, jsonify
from odyssey.v1.auth.functions import get_current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool
from odyssey.v1.form import register_blueprint_v1
from odyssey import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(register_blueprint_v1)


@app.before_request
def before_request():
    if not request.endpoint:
        abort(404)
    if 'api/v1/forms' not in request.endpoint:
        g.user = get_current_user()


@manager.command
def runserver():
    """ overridding the runserver command
    """
    app.run(host='0.0.0.0', port=8001, debug=False)


@manager.command
def drop_all():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.option('--bind', help='Specify Bind')
def create_all(bind):
    """Creates database tables"""
    db.create_all(bind=bind)


if __name__ == '__main__':
    manager.run()

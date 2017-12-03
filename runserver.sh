#!/bin/bash
gunicorn -k flask_sockets.worker -w 3 manage:app -p runserver.pid -b 0.0.0.0:8000 --reload --timeout 300

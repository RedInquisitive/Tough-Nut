#!/bin/bash
export FLASK_APP=/root/ToughNut/toughNut.py
export FLASK_ENV=development
export WERKZEUG_DEBUG_PIN=off
/opt/rh/rh-python36/root/usr/bin/flask run --host=0.0.0.0 --port=80

#!/bin/bash
export FLASK_APP=toughNut.py
export FLASK_ENV=development
export WERKZEUG_DEBUG_PIN=off
flask run --host=0.0.0.0 --port=5000

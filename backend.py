from flask import session, request
from models import State, Base
from data import db
import time
import bcrypt
import requests

timeMax = 15 * 60
referer = "//localhost:5000/" #UPDATE to LIVE DOMAIN

def ip():
	return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def userLogin(user, password):
	session["login"] = "True"
	session["user"] = user
	session["ip"] = ip()
	session["time"] = time.time()
	return True #UPDATE to LDAP

def userLogout():
	session["login"] = "False"
	session["user"] = ""
	session["ip"] = ""
	session["time"] = 0
	
def userAuthorized():
	if ("login" in session 
		and "user" in session 
		and "ip" in session
		and "time" in session
		and session["login"] == "True" 
		and session["user"] != ""
		and session["ip"] == ip()
		and session["time"] > time.time() - timeMax
		and referer in request.headers.get("Referer")):
		return True
	else:
		userLogout()
		return False

def userAccess(dir):
	if (dir == "north" or dir == "south" or dir == "east" or dir == "west"):
		r = requests.get("http://localhost/openDoor.php?doorID=" + session["user"] + "&accessID=" + dir) #UPDATE to URL
		return r.content == "true"
	return False

def currentState():
	return db.session.query(State).all()

def swap(dir, type):
	state = db.session.query(State).filter(State.key==(dir + type)).scalar()

	if state is None:
		return False

	if state.state == "0":
		state.state = "1"
	else:
		state.state = "0"

	db.session.commit()
	return True

def disable(dir, type):
	state = db.session.query(State).filter(State.key==(dir + type)).scalar()

	if state is None:
		return False

	state.state = "0"
	db.session.commit()
	return True
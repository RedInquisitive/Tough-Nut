from flask import session
from models import User, State, Base
from data import db
import bcrypt

def userExists(user):
	return db.session.query(User.id).filter_by(uname=user).scalar() is not None

def userAdd(user, password, fName, lName):
	if userExists(user):
		return False

	hashword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
	db.session.add(User(uname=user, first=fName, last=lName, password=hashword))
	db.session.commit()
	return True

def userLogin(user, password):
	ent = db.session.query(User).filter(User.uname==user).scalar()

	if ent is None:
		return False

	if bcrypt.checkpw(password.encode('utf8'), ent.password.encode('utf8')):
		session["login"] = "True"
		session["user"] = user
		return True

	return False

def userLogout():
	session["login"] = "False"
	session["user"] = ""
	
def userAuthorized():
	if ("login" in session 
		and "user" in session 
		and session["login"] == "True" 
		and session["user"] != ""):
		if userExists(session["user"]):
			return True
		else:
			userLogout()
			return False

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

def do(dir):
	return swap(dir, "door")

def ha(dir):
	return swap(dir, "hall")
from flask import Flask, redirect, render_template, request, session, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from models import State, Base
from data import db
import backend 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thecellar:thecellar@localhost:3306/thecellar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'U9Xx4C8qCPdg13PR3k0byq2Bv70thfwR'
db.init_app(app)

def loc(status, dir, type):
	for elem in status:
		if elem.key == (dir + type):
			return elem.state
	return "?"

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login/")
def login():
	return render_template('login.html')

@app.route("/logout/")
def logout():
	backend.userLogout()
	return redirect(url_for('login'))

#Authenticate a user
@app.route('/check/', methods=['POST'])
def check():
	result = request.form
	success = backend.userLogin(result['uname'], result['password'])
	if success:
		return redirect(url_for('map'))
	else:
		return render_template('error/400.html', message="Wrong user name or password")

#User main view
@app.route("/map/")
def map():
	if backend.userAuthorized():
		stat = backend.currentState()
		#I hate myself for doing this but I just want this done
		ndo = loc(stat, "north", "door")
		nal = loc(stat, "north", "alarm")
		sdo = loc(stat, "south", "door")
		sal = loc(stat, "south", "alarm")
		edo = loc(stat, "east", "door")
		eal = loc(stat, "east", "alarm")
		wdo = loc(stat, "west", "door")
		wal = loc(stat, "west", "alarm")
		return render_template('map.html', ndo=ndo, nal=nal, sdo=sdo, sal=sal, edo=edo, eal=eal, wdo=wdo, wal=wal)
	else:
		return redirect(url_for('login'))

@app.route("/door/<string:dir>")
def door(dir):
	if backend.userAuthorized() and backend.userAccess(dir):
		result = backend.swap(dir, "door")
		if result:
			return render_template('error/200.html', message="OK"), 200
		else:
			return render_template('error/400.html', message="Bad door specified"), 400
	return render_template('error/403.html', message="Contact a system administrator to add your account to Access Control"), 403
	
@app.route("/alarm/<string:dir>")
def alarm(dir):
	if backend.userAuthorized():
		result = backend.disable(dir, "alarm")
		if result:
			return render_template('error/200.html', message="OK"), 200
		else:
			return render_template('error/400.html', message="Bad alarm specified"), 400
	return render_template('error/403.html', message="Contact a system administrator to add your account to Access Control"), 403

#Static pages
@app.route("/about/")
def about():
	return render_template('about.html')

@app.route("/command/<string:name>/")
def command(name):
	print("An attempt to run '" + name + "' was made!")
	return render_template('error/402.html', message="um no u"), 402

@app.route("/command/<string:name>/<string:args>/")
def commandArgs(name, args):
	print("An attempt to run '" + name + "' with '" + args + "' was made!")
	return render_template('error/402.html', message="um no u"), 402

@app.route("/ip/")
def debug():
	return render_template('error/200.html', message="ip: " + session["ip"]), 200

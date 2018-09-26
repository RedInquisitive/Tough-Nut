from flask import Flask, redirect, render_template, request, session, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User, State, Base
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

#Create a new user
@app.route('/user/', methods=['POST'])
def user():
	pin = '991257'
	result = request.form
	if not result['admin_pin'] == pin:
		return render_template('error/400.html', message="Pin wrong")

	uname = result['display_name']
	fname = result['first_name']
	lname = result['last_name']
	password = result['password']
	password2 = result['password_confirmation']
	
	max = 30
	if len(uname) > max or len(fname) > max or len(lname) > max or len(password) > max:
		return render_template('error/400.html', message="fields should be less than " + max + " characters")

	min = 2
	if len(uname) <= min or len(fname) <= min or len(lname) <= min or len(password) <= min:
		return render_template('error/400.html', message="fields should be greater than " + min + " characters")	

	if len(password) < 10:
		return render_template('error/400.html', message="password should be at least 10 characters")

	if password != password2:
		return render_template('error/400.html', message="passwords do not match")

	success = backend.userAdd(uname, password, fname, lname)
	
	if success:
		return redirect(url_for('login'))

	return render_template('error/400.html', message="Display name " + result['display_name'] + " taken.")

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
		nd = loc(stat, "north", "door")
		nh = loc(stat, "north", "hall")
		sd = loc(stat, "south", "door")
		sh = loc(stat, "south", "hall")
		ed = loc(stat, "east", "door")
		eh = loc(stat, "east", "hall")
		wd = loc(stat, "west", "door")
		wh = loc(stat, "west", "hall")
		return render_template('map.html', nd=nd, nh=nh, sd=sd, sh=sh, ed=ed, eh=eh, wd=wd, wh=wh)
	else:
		return redirect(url_for('login'))

@app.route("/door/<string:dir>")
def door(dir):
	if backend.userAuthorized():
		result = backend.do(dir)
		if result:
			return render_template('error/200.html', message="OK"), 200
		else:
			return render_template('error/400.html', message="Bad door specified."), 400
	return redirect(url_for('login'))

@app.route("/hall/<string:dir>")
def hall(dir):
	if backend.userAuthorized():
		result = backend.ha(dir)
		if result:
			return render_template('error/200.html', message="OK"), 200
		else:
			return render_template('error/400.html', message="Bad hall specified."), 400
	return redirect(url_for('login'))

#Static pages
@app.route("/about/")
def about():
	return render_template('about.html')

@app.route("/signup/")
def signup():
	return render_template('signup.html')

@app.route("/command/<string:name>/")
def command(name):
	print("An attempt to run " + name + " was made!")
	return render_template('error/402.html', message="um no u"), 402

@app.route("/command/<string:name>/<string:args>/")
def commandArgs(name, args):
	print("An attempt to run '" + name + "' with '" + args + "' was made!")
	return render_template('error/402.html', message="um no u"), 402

@app.route("/door/")
def dor():
	return render_template('error/400.html', message="You need to specify what door."), 400
	
@app.route("/hall/")
def hal():
	return render_template('error/400.html', message="You need to specify what hall."), 400

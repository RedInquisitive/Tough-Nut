#from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, redirect_back
from flask import *
import subprocess
import requests
import backend 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cdc@localhost/theCellar'
db = SQLAlchemy(app)
db.init_app(app)
#Bootstrap(app)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/about/")
def about():
	return render_template('about.html')

#TODO find 
#stat = [False]*8
#stat = ["1","1","1","potato","0","0","0","0"]

@app.route("/map/", methods=['POST', 'GET'])
def map():
	#check to see if user is logged in
	if request.cookies.get('loggedIn'):
		stat = backend.currentState()		
		print("BACKEND STATUS ************************************")
		print(stat)
		return render_template('map.html', status=stat)
	else:
		return render_template('login.html')

@app.route('/user/', methods=['POST', 'GET'])
def user():
	pin = '0000'

	if request.method == 'POST':
		result = request.form
		print(result)
		if result['admin_pin'] == pin:
			success = backend.addUser(result['display_name'], result['password'], result['first_name'], result['last_name'])
			if success:
				stat = backend.currentState()
				print(stat)
				return render_template('map.html', status=stat)
			else:
				return render_template('error.html', name=result['display_name'])
	url = "64.5.53.50"
	display_name=result['display_name']
	requests.get("http://"+url+'/add.php?stuff=northdoor,' + display_name).content
	requests.get("http://"+url+'/add.php?stuff=southdoor,' + display_name).content
	requests.get("http://"+url+'/add.php?stuff=eastdoor,' + display_name).content
	requests.get("http://"+url+'/add.php?stuff=westdoor,' + display_name).content
	username = request.cookies.get('username')
	return render_template('userProfile.html', name=username)


@app.route('/check/', methods=['POST', 'GET'])
def check():
	if request.method == 'POST':
		result = request.form
		print("Are you here?")
		print(result)
		success = backend.checkPassword(result['uname'], result['password'])
		print("after backend check")
		print(success)
		if success:
			print(result['uname'])
			username = backend.userForEmail(result['uname'])
			#TODO make redirect not render
			#resp = make_response()
			resp = make_response(redirect(url_for('map'),302), 302)
			resp.set_cookie('loggedIn', 'True')
			resp.set_cookie('username', username)
			#print(request.cookies.get('username'))
			#print(request.cookies.get('loggedIn'))
			return resp
			#return redirect(url_for('map'),302,resp)
		else:
			return render_template('error.html')#, name=result['display_name'])


@app.route("/signup/")
def signup():
	return render_template('signup.html')

@app.route("/login/")
def login():
	return render_template('login.html')

@app.route("/Test/")
def test():
	return render_template('Test.html')
		
@app.route("/command/<string:name>/")
def command(name):
	return render_template(
		'cmd.html', cmd=subprocess.check_output(name))

@app.route("/command/<string:name>/<string:args>/")
def commandArgs(name):
	return render_template(
		'cmd.html', cmd=subprocess.check_output([name,args]))

@app.route("/door/")
def dor():
	return render_template('error.html')
	
@app.route("/hall/")
def hal():
	return render_template('error.html')
	

@app.route("/mapabout")
def mapabout():
	return redirect(url_for('map'))

@app.route("/door/<string:dir>", methods=['POST','GET'])
def door(dir):
	print(dir)
	result = backend.do(dir)
	if result:
		return redirect(url_for('map'),205)
	else:
		print("TODO make an error page")
	
@app.route("/hall/<string:dir>", methods=['POST','GET'])
def hall(dir):
	print(dir)
	result = backend.ha(dir)
	if result:
		return redirect(url_for('map'),302)
	else:
		print("TODO make an error page")

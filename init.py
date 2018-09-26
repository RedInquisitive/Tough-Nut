from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User, State, Base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thecellar:thecellar@localhost:3306/thecellar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base.metadata.drop_all(bind=db.engine)
Base.metadata.create_all(bind=db.engine)
db.session.add(State(key="northdoor", state="0"))
db.session.add(State(key="southdoor", state="0"))
db.session.add(State(key="eastdoor", state="0"))
db.session.add(State(key="westdoor", state="0"))
db.session.add(State(key="northhall", state="0"))
db.session.add(State(key="southhall", state="0"))
db.session.add(State(key="easthall", state="0"))
db.session.add(State(key="westhall", state="0"))
db.session.commit()
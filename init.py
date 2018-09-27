from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import State, Base

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
db.session.add(State(key="northalarm", state="0"))
db.session.add(State(key="southalarm", state="0"))
db.session.add(State(key="eastalarm", state="0"))
db.session.add(State(key="westalarm", state="0"))
db.session.commit()
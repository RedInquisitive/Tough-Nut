from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class State(Base):
	__tablename__ = 'states'

	id = Column(Integer, primary_key=True)
	key = Column(String(30), unique=True)
	state = Column(String(30))

	def __repr__(self):
		return '<State %r>' % (self.key)
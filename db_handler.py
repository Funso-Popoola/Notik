import sqlite3
from flask import Flask
from contextlib import closing

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as db_file:
			db.cursor().executescript(db_file.read())
		db.commit()


def tear_down(self):
	pass

def insert(self):
	pass

def update(self):
	pass

def delete(self):
	pass

def read(self):
	pass
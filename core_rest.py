from flask import Flask, jsonify, make_response, abort, g, request, url_for, render_template, flash, redirect
import sqlite3
#from flask.ext.httpauth import HTTPBasicAuth
from contextlib import closing

#configuration
DATABASE = '/tmp/notik.db'
DEBUG = True
SECRET_KEY = 'germane'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#auth = HTTPBasicAuth()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as db_file:
			db.cursor().executescript(db_file.read())
		db.commit()


def insert(values_list):
	g.db.execute('insert into notes (title, content, datetime) values (?, ?, ?)', values_list)
	g.db.commit()
	flash("New note item has been added")


def update():
	pass

def delete():
	pass

def read_all_notes():
	m_cursor = g.db.execute('select id, title, content, datetime from notes order by datetime desc')
	result_list = []
	for row in m_cursor.fetchall():
		result_list.append(dict([['id', row[0]], ['title', row[1]], ['content', row[2]], ['datetime', row[3]]]))
	return result_list

@app.before_request
def prepare():
	g.db = connect_db()


"""The landing page when the api is not in use;
 - displaying the current notes in the database with a button to delete or modify them
 - including a form for new note creation.
 """
@app.route("/")
def index():
	current_notes = read_all_notes()
	return render_template('show_notes.html', notes=current_notes)


@app.route("/insert", methods=["POST"])
def add_new_note():
	values_list = [request.form['title'], request.form['content'], '2014']
	insert(values_list)
	return redirect( url_for("index"))

@app.route("/api/v1.0/add/", methods=["POST"])
def insert_note():
	pass

"""
This enables users to get all the current notes using a GET request
SELECT *
"""
@app.route("/api/v1.0/notes", methods=["GET"])
def get_all_notes():
	abort(404)

"""
Getting a specific note by supplying its id
SELECT where id
"""
@app.route("/api/v1.0/<int:note_id>", methods=["GET"])
#@auth.login_required
def get_specific_note(note_id):
	abort(404)

"""
Accessing and updating an existing note
"""
@app.route("/api/v1.0/<int:note_id>")
def update_note(note_id):
	abort(404)


@app.teardown_request
def teardown(exception):
	db = getattr(g, 'db', None)
	if (not db is None):
		db.close()

@app.errorhandler(404)
def report_error(error):
	res = {'error': 'Not Found'}
	return make_response(jsonify(res), 404)

"""
@auth.get_password
def veryfy_user(username):
	pass

@auth.error_handler
def report_unauthorized():
	res = {'error': 'Unauthorized user'}
	return make_response(jsonify(res), 401)
"""

if __name__ == '__main__':
	app.debug = True
	app.run()
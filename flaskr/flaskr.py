#all the imports
from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create our little application
app = Flask(__name__)
app.config.from_object(__name__)
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('flaskr/schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select * from guests')
	entries = [dict(id = row[0], name = row[1]) for row in cur.fetchall()]
	return render_template('hello.html', entries = entries)

@app.route('/', methods = ['POST'])
def add_entry():
	g.db.execute('insert into guests(name) values(?)', [request.form['name']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()
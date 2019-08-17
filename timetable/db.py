import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
	db = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='usth_timetable'
	)

	cursor = db.cursor()

	with current_app.open_resource('schema.sql') as f:
		sql_file = f.read().decode('utf8')
		queries = sql_file.split(';')

		for query in queries:
			try:
				if query.strip() != '':
					cursor.execute(query.strip())
			except IOError:
				print("Command skipped")

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables"""
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
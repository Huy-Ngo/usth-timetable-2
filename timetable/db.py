import mysql.connector
import json

import click
from flask import current_app, g, jsonify
from flask.cli import with_appcontext

username = ''
password = ''


with open('timetable/auth/database_auth.json', 'r') as f:
	dat = json.load(f)
	username = dat['username']
	password = dat['password']


def init_db():
	db = mysql.connector.connect(
		host='localhost',
		user=username,
		passwd=password,
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


# HTTP requests
def get(table_name, request_body=None):
	""" GET Request
	Get by id:
	request body: {
		'id': int
	}
	Get by name: {
		'name': string
	}
	"""
	db = mysql.connector.connect(
		host='localhost',
		user=username,
		passwd=password,
		database='usth_timetable'
	)

	cursor = db.cursor()

	if request_body is None:
		query = 'SELECT * FROM {}'.format(table_name)
		try:
			cursor.execute(query)
		except mysql.connector.Error as err:
			print(err)
		result = cursor.fetchall()
	else:
		if 'id' in request_body:
			query = 'SELECT * FROM {} WHERE {} = {}'.format(table_name, 'id', request_body['id'])
		elif 'username' in request_body:
			query = 'SELECT * FROM {} WHERE {} = {}'.format(table_name, 'username', request_body['username'])
		elif 'name' in request_body:
			query = 'SELECT * FROM {} WHERE {} = {}'.format(table_name, 'name', request_body['name'])
		else:
			return {}, 400
		try:
			cursor.execute(query)
		except mysql.connector.Error as err:
			print(err)
		result = cursor.fetchone()

	if len(result) == 0:
		return {}, 404

	return result, 200


def post(table_name, request_body):
	""" Add events on update """
	db = mysql.connector.connect(
		host='localhost',
		user=username,
		passwd=password,
		database='usth_timetable'
	)

	# makes sure every values is string
	for param in request_body:
		if type(request_body[param]) is not str:
			request_body[param] = str(request_body[param])

	cursor = db.cursor()
	query = 'INSERT INTO {} ('.format(table_name)
	params = ', '.join(request_body)
	query += params + ') VALUES ('
	values = ', '.join(request_body.values())
	query += values + ')'

	try:
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as err:
		print(err)

	request_body['id'] = cursor.lastrowid
	return request_body, 201


def put(table_name, item_id, request_body):
	db = mysql.connector.connect(
		host='localhost',
		user=username,
		passwd=password,
		database='usth_timetable'
	)

	cursor = db.cursor()

	query = 'UPDATE {} SET'.format(table_name)
	for param in request_body:
		if param == 'id':
			return {}, 403
		query += '{} = \"{}\",'.format(param, request_body[param])

	query = query[:-1]
	query += 'WHERE id = {}'.format(item_id)
	try:
		cursor.execute(query)
	except mysql.connector.Error as err:
		print(err)

	db.commit()
	cursor.execute('SELECT * FROM {} WHERE id = {}'.format(table_name, item_id))
	response = cursor.fetchone()
	return response, 200


def delete(table_name, item_id):
	db = mysql.connector.connect(
		host='localhost',
		user=username,
		passwd=password,
		database='usth_timetable'
	)

	cursor = db.cursor()

	query = 'DELETE FROM {} WHERE id = {}'.format(table_name, item_id)

	cursor.execute(query)
	db.commit()
	return 200


@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables"""
	init_db()
	click.echo('Initialized the database.')


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

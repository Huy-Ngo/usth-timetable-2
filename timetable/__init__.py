import os
from flask import Flask, jsonify, request, abort

from . import request_handler as req
from http import HTTPStatus


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	# @app.route('/')
	# def index():
	# 	return jsonify({})

	from . import updater

	# GET routes
	# @app.route('/<timetable_id>/<view>/<int:year>/<int:month>/<int:day>', methods=['GET'])
	# def r_timetable(timetable_id, view, year, month, day):
	# 	timetable, status_code = updater.get_event(timetable_id, view, year, month, day)
	# 	return jsonify({
	# 		'response': timetable,
	# 		'status_code': status_code
	# 	})

	@app.route('/create', methods=['POST'])
	def create_timetable():
		if not request.json \
				or 'name' not in request.json \
				or 'calendar_id' not in request.json \
				or 'calendar_name' not in request.json:
			abort(HTTPStatus.BAD_REQUEST)
		request_body = {
			'name': request.json['name'],
			'calendar_id': request.json['calendar_id'],
			'timetable_code': request.json['timetable_code']
		}
		response = db.create('timetable', request_body)
		return jsonify(response)

	@app.route('/<timetable_name>/edit', methods=['POST'])
	def edit_timetable(timetable_name):
		if not request.json:
			abort(400)
		response = db.get({
			'table_name': 'timetable',
			'name': timetable_name
		})
		if response['code'] != HTTPStatus.OK:
			abort(response['code'])
		timetable_id = response['response']['id']
		request_body = {
			'calendar_id': request.json['calendar_id'],
			'timetable_code': request.json['timetable_code']
		}
		response = db.update('timetable', timetable_id, request_body)
		return jsonify(response)

	# Log in?
	from . import student_auth
	app.register_blueprint(student_auth.bp)
	# The requests should be reorganized to align with standard

	from . import timetable
	app.register_blueprint(timetable.bp)
	app.add_url_rule('/', endpoint='index')

	return app

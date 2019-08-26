import os
from flask import Flask, jsonify, request


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

	@app.route('/')
	def index():
		return jsonify({})

	from . import updater

	# Get the timetable
	@app.route('/<string:timetable_id>', methods=['GET'])
	def r_timetable(timetable_id):
		timetable = updater.get_event(timetable_id)
		return jsonify(timetable)

	# Log in?
	from . import user_auth
	app.register_blueprint(user_auth.bp)

	return app

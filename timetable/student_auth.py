import functools
from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for, flash
)
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

from http import HTTPStatus

bp = Blueprint('student_auth', __name__, url_prefix='/student')


@bp.route('/<int:student_id>', methods=['GET'])
def r_student(student_id):
	student = db.get({
		'table_name': 'student',
		'id': student_id
	})['response']
	error = None
	if student is None:
		error = 'This student does not exist'
	if error is not None:
		flash(error)

	timetable = db.get({
		'table_name': 'timetable',
		'id': student['timetable_id']
	})['response']['timetable_code']
	return render_template('student_auth/student.html', student=student, timetable=timetable)


@bp.route('/register', methods=['GET', 'POST'])
def r_register():
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		timetable_name = request.form['timetable_id']
		error = None

		if not name:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif not timetable_name:
			error = 'Timetable is required.'
		elif db.get({
			'table_name': 'student',
			'name': name}
		)['code'] == HTTPStatus.OK:
			error = 'User {} is already registered.'.format(name)
		elif db.get({
			'table_name': 'timetable',
			'name': timetable_name}
		)['code'] != HTTPStatus.OK:
			error = 'This timetable does not exist.'

		if error is None:
			timetable = db.get({
				'table_name': 'timetable',
				'name': timetable_name
			})['response']
			timetable_id = timetable['id']

			db.create('student', {
				'name': name,
				'password': generate_password_hash(password),
				'timetable_id': timetable_id
			})
			return redirect(url_for('student_auth.r_login'))

		flash(error)

	return render_template('student_auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def r_login():
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']

		error = None
		response = db.get({
			'table_name': 'student',
			'name': name
		})
		student = None

		if response['code'] == HTTPStatus.NOT_FOUND:
			error = 'Incorrect username.'
		else:
			student = response['response']
			if not check_password_hash(student['password'], password):
				error = 'Incorrect password.'

		if error is None:
			response = db.get({
				'table_name': 'timetable',
				'id': student['timetable_id']
			})
			timetable = response['response']

			session.clear()
			session['student_id'] = student['id']
			# FIXME: redirect to "today" calendar, view is preferred view, saved in local storage
			return redirect(url_for('timetable/index', timetable_id=timetable, view='week', day=6, month=9, year=2019))

		flash(error)

	return render_template('student_auth/login.html')


@bp.before_app_request
def load_logged_in_student():
	student_id = session.get('student_id')

	if student_id is None:
		g.student = None
	else:
		g.student = db.get({
			'table_name': 'student',
			'id': student_id
		})['response']


@bp.route('/logout')
def r_logout():
	session.clear()
	return redirect(url_for('index'))


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.student is None:
			return redirect(url_for('student_auth.r_login'))

		return view(**kwargs)

	return wrapped_view


@bp.route('/<int:student_id>/edit', methods=['GET', 'PUT'])
@login_required
def r_edit_student(student_id):
	if request.method == 'PUT':
		req = request.args
		response = db.get({
			'table_name': 'student',
			'id': student_id
		})
		error = None

		if response['code'] is None:
			error = 'User does not exist.'
		else:
			student = response['response']
			if not check_password_hash(student['password'], req['password']):
				error = 'You cannot edit this student.'

		if error is not None:
			flash(error)

		db.update('student', student_id, req)
		return redirect(url_for('student_auth.r_student'))

	return render_template('student_auth/edit.html')


# FIXME: Send and email to confirm password change request
@bp.route('/<int:student_id>/change_password', methods=['GET', 'PUT'])
@login_required
def r_change_password(student_id):
	if request.method == 'PUT':
		req = request.args
		response = db.get({
			'name': 'student',
			'id': student_id
		})
		error = None

		if response['code'] == HTTPStatus.NOT_FOUND:
			error = 'User does not exist.'
		else:
			student = response['response']
			if not check_password_hash(student['password'], req['old_password']):
				error = 'You cannot edit this student.'

		if error is not None:
			flash(error)

		db.update('student', student_id, {
			'password': generate_password_hash(req['new_password'])
		})
		return redirect(url_for('student_auth.r_student'))

	return render_template('student_auth/change_password.html')

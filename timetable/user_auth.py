import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from timetable.db import get, post

bp = Blueprint('user_auth', __name__, url_prefix='/user_auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		school_id = request.form['school_id']
		timetable_id = request.form['timetable_id']

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif get('student', {'username': username})[1] != 404:
			error = 'This username is already registered'

		if error is None:
			post('student', {
				'username': username,
				'password': generate_password_hash(password),
				'school_id': school_id,
				'timetable_id': timetable_id
			})

		flash(error)

	return render_template('user_auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		error = None
		user, _ = get('student', {'username': username})

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))  # change to relevant timetable later

	return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get('student', {'username': user_id})


@bp.route('/logout')
def logout():
	session.clear()
	return  redirect(url_for('index'))


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view
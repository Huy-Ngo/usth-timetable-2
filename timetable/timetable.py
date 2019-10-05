import datetime

from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from timetable.student_auth import login_required
from . import db, updater

bp = Blueprint('timetable', __name__)


@bp.route('/', methods=['GET'])
def index():
	user_id = session.get('user_id')

	if user_id is None:
		return render_template('timetable/index.html')
	else:
		response = db.get({
			'table_name': 'student',
			'id': user_id
		})
		user_calendar_id = response['response']['timetable_id']

		return  redirect(url_for('r_calendar_view_now', calendar_id=user_calendar_id))


@bp.route('/<calendar_id>', methods=['GET'])
def r_calendar_view_now(calendar_id):
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	day = datetime.datetime.now().day
	view = 'day'  # later: replace it with personal preferred view. Preferred view is saved in cookie/local storage
	return redirect(url_for('timetable.r_list_schedule', timetable_id=calendar_id, view=view, year=year, month=month, day=day))


@bp.route('/<timetable_id>/<view>/<int:year>/<int:month>/<int:day>', methods=['GET'])
def r_list_schedule(timetable_id, view, year, month, day):
	response = updater.get_event(timetable_id, view, year, month, day)

	return render_template(
		'timetable/timetable.html', events=response['response'],
		calendar_id=timetable_id, year=year,
		month=month, day=day, view=view
	)

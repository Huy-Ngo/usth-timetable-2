from __future__ import print_function
import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Time constants
DAY = datetime.timedelta(days=1)
HOUR = datetime.timedelta(hours=1)
MINUTE = datetime.timedelta(minutes=1)


def authorize():
	"""Authorize the app by either using token or making token from credentials.json file"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('timetable/auth/token.pickle'):
		with open('timetable/auth/token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			print("Getting from credentials.json")
			flow = InstalledAppFlow.from_client_secrets_file(
				'timetable/auth/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('timetable/auth/token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds


def load_db(service, calendar_id='primary'):
	""" This will load data from Google API, given calendar id
	Parameters:
	service:
		The service variable that is built from credentials variable
	calendar_id:
		default value: 'primary'
		The id of a calendar, must be updated manually
	"""
	now = datetime.datetime.utcnow()
	begin = None
	end = None
	if now.day >= 8:
		begin = datetime.datetime(year=now.year, month=8, day=15)
		end = datetime.datetime(year=now.year+1, month=7, day=31)

	begin = begin.isoformat() + 'Z'  # 'Z' indicates UTC time
	end = end.isoformat() + 'Z'

	events_result = service.events().list(
		calendarId=calendar_id, timeMin=begin,
		timeMax=end, singleEvents=True,
		orderBy='startTime').execute()

	events = events_result.get('items', [])

	print("Events from {} to {}\n".format(begin, end))

	# This is for development stage. When DB is integrated, it should returns a message (?)
	return events


def print_event(event):
	"""" This function is used for cli testing only """
	if event['start'].get('dateTime') is None:
		return
	start = event['start'].get('dateTime')
	print(start, event['summary'])


def get_event(calendar_id='ict2'):
	""" This one use a calendar code and get that events
	"""
	creds = authorize()

	service = build('calendar', 'v3', credentials=creds)

	# Call the Calendar API
	with open('timetable/calendar_list.json', 'r') as f:
		calendar_list = json.loads(f.read())
		calendar = calendar_list[calendar_id]
		events = load_db(service, calendar)

		for event in events:
			if event['start'].get('dateTime') is None:
				continue
			if 'location' in event:
				event['summary'] += ' - {}'.format(event['location'])

	return events


if __name__ == '__main__':
	get_event()

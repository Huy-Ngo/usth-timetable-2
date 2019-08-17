from __future__ import print_function
import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from flask import jsonify

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

def update_db(service, calendar_id='primary'):
	"""Update the database by retrieving data from Google API and write it to the server's db
	Parameters:
	service:
		The service variable that is built from credentials variable
	calendar_id:
		default value: 'primary'
		The id of a calendar, must be updated manually
	"""
	now = datetime.datetime.utcnow()
	last_week = now - 7 * DAY
	next_week = now + 7 * DAY

	last_week = last_week.isoformat() + 'Z' # 'Z' indicates UTC time
	next_week = next_week.isoformat() + 'Z'

	events_result = service.events().list(calendarId=calendar_id, timeMin=last_week,
										timeMax=next_week, singleEvents=True,
										orderBy='startTime').execute()

	events = events_result.get('items', [])

	print("Events from {} to {}\n".format(last_week, next_week))

	# This is for development stage. When DB is integrated, it should returns a message (?)
	return events

def print_event(events):
	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		print(start, event['summary'])

def main():
	""" Update database and show events
	Events updated from last week to next week
	"""
	creds = authorize()

	service = build('calendar', 'v3', credentials=creds)

	# Call the Calendar API
	# events = update_db(service, 'fmapuhshmsgpbtu2ljlvvq3pps@group.calendar.google.com')
	calendar_list = {}
	with open('timetable/calendar_list.json') as f:
		calendar_list = jsonify(f.read())
		for calendar in calendar_list:
			events = update_db(service, calendar_list[calendar])
			print(calendar)
			print_event(events)

	# print_event(events)

if __name__ == '__main__':
	main()
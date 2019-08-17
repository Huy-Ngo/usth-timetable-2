# USTH Timetable API

## Description

This project is started in order to make checking timetable more convenient for students of USTH.

## Idea

Since the timetable is based on Google calendar, this project will use Google calendar API to get the data from Google and let the user read that in an easier way. This is an API written to serve that app.

## Features

Users of this API can get: customized schedule between two points in time

## Parameters

- `string[] classes`: The classes the person wants to query. Default: The classes that the person is in.
- `string timeStart`: The start of the period in ISO 8601. Default: Now. Minimum: Now - 1 week.
- `string timeEnd`: The end of the period in ISO 8601. Default: Now + 24 hours. Maximum: Now + 1 week.

Example: `:/ict2/2019-27-07/2019-10-08/`

## Return Object

```
eventList{
	event{
		datetime TimeStart
		datetime TimeEnd
		string Subject
		string Location
	}
}
```
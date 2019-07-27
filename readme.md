# USTH Timetable API

## Description

This project is started in order to make checking timetable more convenient for students of USTH.

## Idea

Since the timetable is based on Google calendar, this project will use Google calendar API to get the data from Google and let the user read that in an easier way. This is an API written to serve that app.

## Features

Users of this API can get: customized schedule between two points in time

## Parameters

- `int userId`: The ID of the user.
- `string[] classes`: The classes the person wants to query. Default: The classes that the person is in.
- `datetime timeStart`: The start of the period. Default: Now
- `datetime timeEnd`: The end of the period. Default: Now + 24 hours

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
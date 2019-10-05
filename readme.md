# USTH Timetable

## Description

This project is started in order to make checking timetable more convenient for students of USTH.

This starts out as an API but as it's being developed, I've decided to turn it into a full app.

## Features

Users of this app can see their timetable they signed up for. For computer users, they can see their schedule in a week, while mobile users can see in three days (yesterday, today, and tomorrow)

## Usage

### GET timetable

Parameters, in order:

- `string class`: The class the person wants to query. Default: The class that the person is in.
- `string view`: The type of view: year, month, week, day, agenda. Default: week (desktop), agenda (mobile)
- `int year`
- `int month`
- `int day`: default: today

E.g. `:/ict2/week/2019/8/28`

Return object:
```
eventList[
	event{
		datetime TimeStart
		datetime TimeEnd
		string Event Summary
	}
]
```

### GET student

Parameter:

- `string username`: The username the student signed up as.

E.g. `:/user/huy%20ngo`

Return object:
```
Student{
    int id
    string username
    string school_id
    int timetable_id
}
```

### POST timetable
Require admin authorization

URLs: 

- `:/create`: Create a new timetable
- `:/<timetable_name>/edit`: Edit meta info about a timetable

Parameter:

```
{
    int id
    string name
    string calendar_id
    string calendar_name
}
```


### POST student
Require admin authorization or user request

URLs:

- `:/user/register`: create new account
- `:/user/login`: log in to an account
- `:/user/logout`: log out of an account
- `:/user/<user_id>/edit`: edit the details of an account
- `:/user/<user_id>/change_password`: change the password of an account

Parameter:
```
{
    int id
    string username
    string password
    string school_id
    string calendar_id
}
```
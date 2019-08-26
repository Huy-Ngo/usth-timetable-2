DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Timetable;

CREATE TABLE Timetable (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(5) NOT NULL UNIQUE,
    calendar_id VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Student (
	id INTEGER AUTO_INCREMENT,
	username VARCHAR(32) UNIQUE NOT NULL,
	password TEXT NOT NULL,
	school_id CHAR(6),
	timetable_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (timetable_id) REFERENCES Timetable(id)
);
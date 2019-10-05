DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Timetable;

CREATE TABLE Timetable (
    id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
    timetable_code VARCHAR(5) NOT NULL UNIQUE, -- such as b1, ict2, amsn3
    calendar_id VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Student (
	id INTEGER AUTO_INCREMENT,
	name VARCHAR(32) UNIQUE NOT NULL,
	password TEXT NOT NULL,
	-- school_id CHAR(6),
	timetable_id VARCHAR(5) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (timetable_id) REFERENCES Timetable(id)
);
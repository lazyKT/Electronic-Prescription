-- SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE user (
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username varchar(15),
password varchar(15),
role varchar(10),
activated BOOLEAN
);

CREATE TABLE pharmacist (
phar_id INTEGER PRIMARY KEY AUTOINCREMENT,
fName TEXT,
lName TEXT,
gender varchar(1),
email TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
    REFERENCES user (user_id)
);

CREATE TABLE doctor (
doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
fName TEXT,
lName TEXT,
gender varchar(1),
email TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
    REFERENCES user (user_id)
);

CREATE TABLE admin (
adm_id INTEGER PRIMARY KEY AUTOINCREMENT,
fName TEXT,
lName TEXT,
email TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
    REFERENCES user (user_id)
); 

CREATE TABLE patient (
pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
fName TEXT,
lName TEXT,
gender varchar(1),
email TEXT,
dob TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
    REFERENCES user (user_id)
); 

CREATE TABLE allergy (
allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
allergy TEXT,
pat_id INTEGER NOT NULL,
FOREIGN KEY (pat_id)
    REFERENCES patient (pat_id)
); 

CREATE TABLE medHistory (
medHist_id INTEGER PRIMARY KEY AUTOINCREMENT,
medHistory TEXT,
pat_id INTEGER NOT NULL,
FOREIGN KEY (pat_id)
    REFERENCES patient (pat_id)
);

CREATE TABLE medicine (
med_id INTEGER PRIMARY KEY AUTOINCREMENT,
medName TEXT,
expDate TEXT,
descrption TEXT,
instruction TEXT,
quantity INTEGER,
price INTEGER
);

CREATE TABLE prescription (
prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
identifier TEXT,
date TEXT,
quantity INTEGER,
doc_id INTEGER NOT NULL,
pat_id INTEGER NOT NULL,
med_id INTEGER NOT NULL,
phar_id INTEGER NOT NULL,
FOREIGN KEY (doc_id)
    REFERENCES doctor (doc_id)
FOREIGN KEY (pat_id)
    REFERENCES patient (pat_id)
FOREIGN KEY (med_id)
    REFERENCES medicine (med_id)
FOREIGN KEY (phar_id)
    REFERENCES pharmacist (phar_id)
);

-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS customers;

PRAGMA foreign_keys=ON;

CREATE TABLE theaters(
	name		TEXT,
	capacity 	INT,
	PRIMARY KEY (name)
);

CREATE TABLE movies(
	title				TEXT,
	production_year 	INT,
	IMDB_key			char(9),
	running_time		INT,
	PRIMARY KEY (IMDB_key)
);

CREATE TABLE performances(
	date 				DATE,
	start_time			TIME, 
	performance_id		TEXT DEFAULT (lower(hex(randomblob(16)))),
	theater 			TEXT,
	IMDB_key			char(8),
	remainingSeats		INT DEFAULT 0,
	PRIMARY KEY (performance_id),
	FOREIGN KEY (theater) REFERENCES theaters(name),
	FOREIGN KEY (IMDB_key) REFERENCES movies(IMDB_key)
);

CREATE TABLE tickets(
	ticket_id 			TEXT DEFAULT (lower(hex(randomblob(16)))),
	performance_id		TEXT,
	user_name 			TEXT,
	PRIMARY KEY (ticket_id),
	FOREIGN KEY (performance_id) REFERENCES performances(performance_id),
	FOREIGN KEY (user_name) REFERENCES customers(user_name)
);


CREATE TABLE customers(
	user_name	TEXT,
	name 		TEXT,
	password	TEXT,
	PRIMARY KEY (user_name)
);


CREATE TRIGGER update_seats BEFORE INSERT ON tickets
BEGIN
	 if performances.remainingSeats < 1
	 	 -->"Can't buy ticket"
	 else
	 	--"buy the ticket"
	

CREATE TRIGGER default_seats AFTER INSERT ON performances
BEGIN
	UPDATE performances
	SET remainingSeats = (SELECT capacity FROM theaters WHERE theaters.name = performances.theater);
END;



INSERT
INTO   theaters(name, capacity)
VALUES ('Kino', '3'),
	   ('Filmstaden', '130'),
	   ('Röda Kvarn', '50'),
	   ('Spegeln', '100');

INSERT
INTO   movies(title, production_year, IMDB_key, running_time)
VALUES ('Little Women', 2020, 'tt3281548', 135),
	   ('Parasite', 2019, 'tt6751668', 132),
	   ('Birds Of Prey', 2020, 'tt7713068', 109);


INSERT
INTO 	performances(date, start_time, theater, IMDB_key)
VALUES ('2020-02-08', '14:00', 'Spegeln', 'tt3281548'), 
	   ('2020-02-08', '18:00', 'Spegeln', 'tt6751668'), 
	   ('2020-02-08', '20:30', 'Spegeln', 'tt7713068'), 
	   ('2020-02-09', '10:00', 'Spegeln', 'tt3281548'), 
	   ('2020-02-09', '14:00', 'Spegeln', 'tt6751668'), 
	   ('2020-02-09', '18:00', 'Spegeln', 'tt7713068'), 
	   ('2020-02-08', '17:00', 'Kino', 'tt6751668'), 
	   ('2020-02-08', '19:30', 'Kino', 'tt3281548');

INSERT
INTO	customers(user_name, name, password)
VALUES ('filip', 'Filip Cederquist', '123123'),
	   ('nellie', 'Nellie Duhs', '123123'),
	   ('tom', 'Tom Richter', '123123'),
	   ('adam', 'Adham Zac', '123123'),
	   ('bertil', 'Bertil Bertilsson', '123123'),
	   ('tomas', 'Tomas Alf', '123123'),
	   ('karin', 'Karin Skarp', '123123');

INSERT
INTO	tickets(performance_id, user_name)
SELECT	performance_id, 'filip'
FROM	performances
WHERE	theater = 'Spegeln' AND IMDB_key = 'tt3281548' AND date = '2020-02-09';

INSERT
INTO	tickets(performance_id, user_name)
SELECT	performance_id, 'tom'
FROM	performances
WHERE	theater = 'Spegeln' AND IMDB_key = 'tt3281548' AND date = '2020-02-09';

INSERT
INTO	tickets(performance_id, user_name)
SELECT	performance_id, 'nellie'
FROM	performances
WHERE	theater = 'Spegeln' AND IMDB_key = 'tt3281548' AND date = '2020-02-09';















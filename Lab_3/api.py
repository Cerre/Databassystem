from bottle import get, post, run, request, response
import sqlite3
import json


HOST = 'localhost'
PORT = 7007

conn = sqlite3.connect("theaters.sqlite")


def url(resource):
    return f"http://{HOST}:{PORT}{resource}"


def format_response(d):
    return json.dumps(d, indent=4) + "\n"


@post('/reset')
def reset():
	query = (
		"""
		DROP table IF EXISTS performances;
		DROP table IF EXISTS theaters;
		DROP table IF EXISTS customers;
		DROP table IF EXISTS tickets;
		DROP table IF EXISTS movies;
	"""
	)
	#f = open("/Users/filipcederquist/Documents/Skolarbete/Databaser/Lab_3/lab2.sql", "r")
	f = open("/Users/filipcederquist/Documents/Skolarbete/Databaser/Lab_3/theaters.sql")
	query += f.read()
	c = conn.cursor()
	c.executescript(query)
	response.status = 200
	return 'OK'


def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@get('/ping')
def ping():
	response.status = 200
	return "pong"


@get('/movies')
def get_movies():
    c = conn.cursor()
    query = (
        """
        SELECT title, IMDB_key, production_year
        FROM   movies
        WHERE 1 = 1
        """
    )
    params = []
    if request.query.title:
    	query += "AND title = ?"
    	params.append(request.query.title)
    if request.query.production_year:
    	query += "AND production_year = ?"
    	params.append(request.query.production_year)
    c.execute(query, params)
    s = [{"title": title, "IMDB_key": IMDB_key, "production_year": production_year}
         for (title, IMDB_key, production_year) in c]
    response.status = 200
    return json.dumps({"data": s}, indent=4)


@post('/performances')
def post_performances():
    response.content_type = 'theaters/json'
    c = conn.cursor()
    query = (
        """
        INSERT INTO performances (IMDB_key, theater, date, start_time)
        VALUES (?,?,?,?);
        """
    )
    params = []
    params.append(request.query.IMDB_key)
    params.append(request.query.theater)
    params.append(request.query.date)
    params.append(request.query.start_time)
    c.execute(query, params)
    
    response.status = 200
    c = conn.cursor()
    c.execute("""
    	SELECT *
    	FROM performances
    	WHERE rowid = last_insert_rowid()
    	""")
    s = [{"IMDB_key": IMDB_key, "theater": theater, "date": date, "start_time": start_time, "performance_id": performance_id}
         for (IMDB_key, theater, date, start_time, performance_id) in c]
    return json.dumps({"data": s}, indent=4)





@get('/performances')
def get_performances():
    response.content_type = 'theaters/json'
    c = conn.cursor()
    query = (
        """
        SELECT performance_id, date, start_time, title, production_year, theater, remainingSeats
        FROM   movies
        JOIN   performances
        USING  (IMDB_key)
        """
        )
    c.execute(query)
    s = [{"performance_id": performance_id, "date": date, "start_time": start_time, "title": title, "year": production_year, "theater": theater, "RemainingSeats": remainingSeats}
         for (performance_id, date, start_time, title, production_year, theater, remainingSeats) in c]
    response.status = 200
    return json.dumps({"data": s}, indent=4)




@get('/theaters')
def get_students():
    response.content_type = 'theaters/json'
    query = """
        SELECT name, capacity
        FROM   theaters
        WHERE  1 = 1
        """
    params = []
    if request.query.name:
        query += "AND name = ?"
        params.append(request.query.name)
    if request.query.capacity:
        query += "AND capacity >= ?"
        params.append(request.query.capacity)
    c = conn.cursor()
    c.execute(
        query,
        params
    )
    s = [{"name": name, "capacity": capacity}
         for (name, capacity) in c]
    response.status = 200
    return format_response({"data": s})





@get('/movies/<IMDB_key>')
def get_student(IMDB_key):
    response.content_type = 'theaters/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT title, production_year, IMDB_key, running_time
        FROM   movies
        WHERE  IMDB_key = ?
        """,
        [IMDB_key]
    )
    s = [{"title": title, "production_year": production_year, "IMDB_key": IMDB_key, "running_time": running_time}
         for (title, production_year, IMDB_key, running_time) in c]
    response.status = 200
    return format_response({"data": s})


@post('/tickets')
def post_ticket():
    response.content_type = 'theaters/json'
    c = conn.cursor()
    #Check password
    c.execute(
        """
        SELECT password
        FROM customers
        WHERE user_name = ?
        """,
        [request.query.user_name])
    password = c.fetchone()[0]
    if password != request.query.pwd:
        return("Wrong password")
    else:

        query = (
            """
            INSERT INTO tickets (user_name, performance_id)
            VALUES (?,?);
            """
        )
        params = []
        params.append(request.query.user_name)
        params.append(request.query.performance_id)
        c.execute(query, params)
        query = ("""
            SELECT user_name, performance_id, ticket_id
            FROM tickets
            WHERE rowid = last_insert_rowid()
                """)
        c.execute(query)
        s = [{"user_name": user_name, "performance_id": performance_id, "ticket_id": ticket_id}
             for (user_name, performance_id, ticket_id) in c]
        response.status = 200
        return format_response({"data": s})




#320c65edb15cf3a0ec6b7a062fec636c



run(host=HOST, port=PORT, debug=True)





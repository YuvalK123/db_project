from server_helper import *


@app.route('/bestScores')
def get_best_scores():
    try:
        cursor = db.cursor()
        query_best_10_scores = "SELECT * FROM score_history ORDER BY score DESC LIMIT 10;"
        cursor.execute(query_best_10_scores)
        result = cursor.fetchall()
        return json.dumps(result, default=datetime_tostring)
    except Exception as e:
        print(e)
        return DatabaseError(e)

@app.route('/admin/best_score')
def get_best_score():
    try:
        cursor = db.cursor()
        best_score_query = "SELECT username, score, datetime FROM users, (SELECT uid, MAX(score) AS " \
                           "score, datetime FROM score_history) AS best_score WHERE users.id = " \
                           "best_score.uid;"
        cursor.execute(best_score_query)
        result = cursor.fetchall()
        if len(result) == 1:
            message = f"{result[0][0]} has the highest score which is {result[0][1]} since {result[0][2]}."
            return message
        else:
            return "0 games were ended"
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/quantity_of_gamers')
def get_number_of_gamers():
    try:
        cursor = db.cursor()
        num_gamers_query = "SELECT COUNT(*) FROM ((SELECT uid FROM games) UNION (SELECT uid FROM " \
                           "score_history)) AS all_gamers;"
        cursor.execute(num_gamers_query)
        result = cursor.fetchone()
        message = f"Number of people playing by far: {result[0][0]}"
        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/age_statistics')
def get_age_statistics():
    try:
        query_avg_score_according_to_ages = "SELECT AVG(score) FROM score_history, users WHERE users.id = " \
                                            "score_history.uid AND users.age BETWEEN %s AND %s;"
        cursor = db.cursor()
        twenty_five_years_ago = datetime.date.today() - relativedelta(years=25)
        cursor.execute(query_avg_score_according_to_ages, (twenty_five_years_ago, datetime.date.today()))
        avg_score_young = cursor.fetchall()[0][0]
        fifty_five_years_ago = datetime.date.today() - relativedelta(years=55)
        cursor.execute(query_avg_score_according_to_ages, (fifty_five_years_ago, twenty_five_years_ago))
        avg_score_adults = cursor.fetchall()[0][0]
        hundred_years_ago = datetime.date.today() - relativedelta(years=100)
        cursor.execute(query_avg_score_according_to_ages, (hundred_years_ago, fifty_five_years_ago))
        avg_score_elders = cursor.fetchall()[0][0]
        avg_score_young = 0 if avg_score_young is None else avg_score_young
        avg_score_adults = 0 if avg_score_adults is None else avg_score_adults
        avg_score_elders = 0 if avg_score_elders is None else avg_score_elders
        message = f"Average score for ages 0-25: {avg_score_young}\nAverage score for ages 26-55: " \
                  f"{avg_score_adults}\n Average score for ages 56-99: {avg_score_elders}"
        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/gender')
def get_gender_statistics():
    try:
        query_gender_score_sum = "SELECT SUM(score) FROM users, score_history WHERE users.id = score_history.uid AND " \
                                 "users.gender = %s;"
        cursor = db.cursor()
        cursor.execute(query_gender_score_sum, ('m', ))
        male_sum = cursor.fetchall()[0][0]
        male_sum = 0 if male_sum is None else male_sum
        cursor.execute(query_gender_score_sum, ('f', ))
        female_sum = cursor.fetchall()[0][0]
        female_sum = 0 if female_sum is None else female_sum
        message = f"Cumulative score for males: {male_sum}\nCumulative score for females: {female_sum}"
        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)



@app.route('/hint')
def get_hint():
    options = ["bornin, diedin, restaurant"]
    try:
        cursor = db.cursor()
        option = random.randint(1, 2)
        country = request.args.get('country')
        country = country_to_id(country)
        query, keyword = get_from_option(option, country)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            record = result[0][0]
            result = f"{record} {keyword} there"
        else:
            query, keyword = get_from_option((option % 2) + 1, country)
            cursor.execute(query)
            result = cursor.fetchone()
            print("result", result)
            if result is None:
                result = "No Available Hint"
            elif len(result) > 0:
                record = result[0]
                result = f"{record} was {keyword} there"
            else:
                result = "No Available Hint"
        return result
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/get_country')
def get_random_country():
    user = request.args.get(GAME_PARAMETERS["user"])
    query = f"SELECT location FROM globalinfoapp.locations WHERE id NOT IN " \
            f"(SELECT location FROM game_locations WHERE gid=(SELECT id FROM games WHERE uid={user} LIMIT 1)) " \
            f"ORDER BY RAND() LIMIT 1;"
    # query = "SELECT location FROM locations ORDER BY RAND() LIMIT 1"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        country = cursor.fetchone()
        if len(country) > 0:
            return country[0]
        return "fail"
    except Exception as e:
        return DatabaseError(e)


@app.route('/movies')
def get_person_movies():
    person = request.args.get('person')
    ret = {"gender": "", "actedIn": [], "directed": []}
    if not person:
        return json.dumps(None)
    try:
        cursor = db.cursor()
        query = f"SELECT id, gender FROM people_info WHERE Name='{person}' LIMIT 1"
        cursor.execute(query)
        record = cursor.fetchone()
        if not record:
            return json.dumps(None)
        pid, ret["gender"] = record
        # get all movies
        query = f"SELECT movieId, job_id FROM people_movies WHERE pid={pid}"
        cursor.execute(query)
        record = cursor.fetchall()  # ((301,0/1), (555,0/1),...)
        if not record:
            return json.dumps(None)
        actor_id, directors_id = "00", "01"
        # print(record)
        actor_movies = tuple((x[0]) for x in record if actor_id in str(x[1]))
        director_movies = tuple(str(x[0]) for x in record if directors_id in str(x[1]))
        a_record, d_record = None, None
        # print(actor_movies, director_movies)
        if len(actor_movies) > 0:
            ret["actedIn"] = movies_record_to_list(cursor, actor_movies)
        if len(director_movies) > 0:
            ret["directed"] = movies_record_to_list(cursor, director_movies)
        print(ret)
    except Exception as e:
        print(e)
        return DatabaseError(e)
    return json.dumps(ret)
    pass


@app.route('/get_people')
def get_all_related():
    country = request.args.get('country')
    born_query = f"SELECT Name FROM people_info WHERE BornIn=(SELECT id FROM locations WHERE location='{country}');"
    died_query = f"SELECT Name FROM people_info WHERE DiedIn=(SELECT id FROM locations WHERE location='{country}');"
    print(born_query)
    print(died_query)
    try:
        cursor = db.cursor()
        cursor.execute(born_query)
        born_country = cursor.fetchall()
        print(born_country)
        born_country = [x[0] for x in born_country]
        cursor.execute(died_query)
        died_country = cursor.fetchall()
        print(died_country)
        died_country = [x[0] for x in died_country]
        b = ",".join(born_country)
        d = ",".join(died_country)
        ret = {"born": b, "died": d}
        print(ret)
        return json.dumps(ret)
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/users', methods=['GET', 'POST'], )
def users():
    username, psw = request.args.get('user'), request.args.get('pass')
    uid, is_admin = -1, False
    if request.method == 'POST':
        gender, age = request.args.get('gender'), request.args.get('age')
        if not gender:
            gender = ''
        if not age:
            age = -1
        query = f"INSERT INTO users (username, password, age, gender) VALUES " \
                     f"('{username}', '{psw}', '{age}', '{gender}');"
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        query = f"SELECT id FROM users WHERE (username='{username}' AND password='{psw}') LIMIT 1;"
        cursor.execute(query)
        record = cursor.fetchone()
        if record:
            uid = record[0]
    else:
        try:
            cursor = db.cursor()
            query = f"SELECT id FROM users WHERE (username='{username}' AND password='{psw}') LIMIT 1;"
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                uid = record[0]
                query = f"SELECT uid from admins WHERE uid={uid} LIMIT 1;"
                cursor.execute(query)
                r = cursor.fetchone()
                if r:
                    is_admin = True
        except Exception as e:
            print("e", e)
    return json.dumps({"uid": uid, "admin": is_admin})


@app.route('/getgame', methods=['GET'])
def get_game():
    user = request.args.get(GAME_PARAMETERS["user"])
    ret_value = {"score": None, "letters": None, "curr_country": None, "strikes": None, "gid": None}
    try:
        cursor = db.cursor()
        query = f"SELECT id, current_score, strikes, current_location FROM games WHERE uid={user};"
        cursor.execute(query)
        game_record = cursor.fetchone()
        if not game_record:
            return json.dumps(None)
        ret_value["gid"], ret_value["score"], ret_value["strikes"], ret_value["curr_country"] = game_record
        ret_value["curr_country"] = id_to_country(ret_value["curr_country"])
        game_id = ret_value["gid"]
        query = f"SELECT letter FROM game_letter WHERE gid={game_id}"
        cursor.execute(query)
        letters_records = cursor.fetchall()
        if letters_records:
            letters = [letter[0] for letter in letters_records]
            ret_value["letters"] = ",".join(letters)

        '''
        query = f"SELECT location FROM globalinfoapp.locations WHERE id IN " \
                f"(SELECT location FROM game_locations WHERE gid={game_id});"
        cursor.execute(query)
        locations_records = cursor.fetchall()
        if locations_records:
            locations = (location[0] for location in locations_records)
            ret_value["countries"] = ", ".join(locations)
        '''
    except Exception as e:
        print(e)
        return DatabaseError(e)
    return json.dumps(ret_value)

@app.route('/gameover')
def delete_game():
    game_id = GAME_PARAMETERS["game"]
    try:
        cursor = db.cursor()
        letters_query = f"DELETE FROM game_letter WHERE gid={game_id}"
        cursor.execute(letters_query)
        locations_query = f"DELETE FROM game_locations WHERE gid={game_id}"
        cursor.execute(letters_query)
        db.commit()
        game_query = f"DELETE FROM games WHERE gid={game_id}"
        cursor.execute(letters_query)
        db.commit()
        return "200"
    except Exception as e:
        print(e)
        return DatabaseError(e)



@app.route('/savegame', methods=['POST'])
def save_game():
    parameters,  cursor = GAME_PARAMETERS, db.cursor()
    args = request.form

    curr_location, countries, letters, strikes, score, user = \
        parameters["curr_country"], parameters["countries"], parameters["letters"], \
        parameters["strikes"], parameters["score"], parameters["user"]

    curr_location, countries, letters, strikes, score, user = \
        args[curr_location], args[countries], args[letters], args[strikes], args[score], args[user]

    print(curr_location, countries, letters, strikes, score, user)
    if str(curr_location) != "-1":
        curr_location = country_to_id(curr_location)
    print("curr location", curr_location)
    get_query = f"SELECT id FROM games WHERE uid={user};"
    cursor.execute(get_query)
    game_record = cursor.fetchone()
    game_exists, game_id = False, -1
    print(game_record)
    if game_record:
        game_exists = True
        game_id = game_record[0]
    if not game_exists:
        game_query = f"INSERT INTO games (uid, current_score, strikes, current_location) VALUES " \
                f"({user}, {score}, {strikes}, {curr_location});"
    else:
        game_query = f"UPDATE games SET current_score = {score}, strikes = {strikes}, " \
                f"current_location = {curr_location} WHERE uid={user};"
        delete_query = f"DELETE FROM game_letter WHERE gid={game_id};"
        cursor.execute(delete_query)
        db.commit()

    cursor.execute(game_query)
    db.commit()
    if not game_exists:
        cursor.execute(get_query)
        game_record = cursor.fetchone()
        game_id = game_record[0]

    # insert letters and locations
    letters_arr, locations = letters.split(","), countries.split(",")
    letters_arr = [(game_id, letter) for letter in letters_arr]
    try:
        if len(letters_arr) > 0:
            query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
            cursor.executemany(query, letters_arr)
        if len(locations) > 0:
            locations_arr = []
            for location in locations:
                locations_arr.append(country_to_id(location))
            locations = [(game_id, location) for location in locations_arr if location is not None]
            query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
            cursor.executemany(query, locations)
        db.commit()
    except Exception as e:
        print(e)
        return DatabaseError(e)
    return str(game_id)


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    """
    requires uid, and username to change username, pass to change password
    """
    if request.method == 'POST':
        username, psw, uid = request.args.get("username"), request.args.get("pass"), request.args.get("uid")
        ret_val = -1
        if username and psw:  # update username and password
            query = f"UPDATE users SET username = '{username}', password = '{psw}' WHERE id={uid};"
        elif username:  # update username
            query = f"UPDATE users SET username = '{username}' WHERE id={uid};"
        elif psw:
            query = f"UPDATE users SET password = '{psw}' WHERE id={uid};"
        else:
            return str(ret_val)
        try:
            cursor = db.cursor()
            ret_val = cursor.execute(query)
            db.commit()
        except Exception as e:
            print(e)
            pass
        return str(ret_val)
    else:
        query = f"SELECT username, password, age, gender FROM users WHERE users.id = {request.args.get('uid')};"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                return {}
            return json.dumps(result[0], default=str)
        except Exception as e:
            print(e)
            return DatabaseError(e)




@app.route('/')
def index():
    return "Welcome to the server"


app.run(debug=True, port=PORT)

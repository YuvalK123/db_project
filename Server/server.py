from server_helper import *


@app.route('/bestScores')
def get_best_scores():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        query_best_10_scores = "SELECT users.username, score_history.score, score_history.datetime FROM " \
                               "score_history, users WHERE score_history.uid=users.id ORDER BY score DESC LIMIT 10;"
        cursor.execute(query_best_10_scores)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(result, default=datetime_tostring)
    except Exception as e:
        print(e)
        return DatabaseError(e)

@app.route('/admin/best_score')
def get_best_score():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        best_score_query = "SELECT username, score, datetime FROM users, (SELECT uid, MAX(score) AS " \
                           "score, datetime FROM score_history) AS best_score WHERE users.id = " \
                           "best_score.uid;"
        cursor.execute(best_score_query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if len(result) == 1:
            message = f"{result[0][0]} has the highest score which is {result[0][1]} since {result[0][2]}.\n"

            return message
        else:
            return "0 games were ended"
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/quantity_of_gamers')
def get_number_of_gamers():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        num_gamers_query = "SELECT COUNT(*) FROM ((SELECT uid FROM games) UNION (SELECT uid FROM " \
                           "score_history)) AS all_gamers;"
        cursor.execute(num_gamers_query)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        message = f"Number of people playing by far: {result[0]}\n"

        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/age_statistics')
def get_age_statistics():
    try:
        db = mysql.connect()
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
                  f"{avg_score_adults}\nAverage score for ages 56-99: {avg_score_elders}\n"
        cursor.close()
        db.close()
        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/admin/gender')
def get_gender_statistics():
    try:
        db = mysql.connect()
        query_gender_score_sum = "SELECT SUM(score) FROM users, score_history WHERE users.id = score_history.uid AND " \
                                 "users.gender = %s;"
        cursor = db.cursor()
        cursor.execute(query_gender_score_sum, ('m', ))
        male_sum = cursor.fetchall()[0][0]
        male_sum = 0 if male_sum is None else male_sum
        cursor.execute(query_gender_score_sum, ('f', ))
        female_sum = cursor.fetchall()[0][0]
        female_sum = 0 if female_sum is None else female_sum
        message = f"Cumulative score for males: {male_sum}\nCumulative score for females: {female_sum}\n"
        cursor.close()
        db.close()
        return message
    except Exception as e:
        print(e)
        return DatabaseError(e)

@app.route('/hint')
def server_hints():
    print("hint")
    country, user = request.args.get('country'), request.args.get('user')
    print(country, user)
    is_new = request.args.get("new")
    fail = {"result": False, "data": "Database Connection lost"}
    if not (user or country):
        fail["data"] = "invalid input"
        return fail
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    if not not is_new:
        hints_query = f"SELECT hints FROM games WHERE uid={user}"
        hints = select_query(query=hints_query, is_many=False, cursor=cursor)
        if not hints:
            fail["data"] = "[No Available Hint]"
            return fail
        amount = hints[0]
    else:
        amount = 3
    country = country_to_id(cursor=cursor, country=country)
    if amount < 1:
        return "No Available Hint"
    # query, keyword = get_from_option(option, country)
    hints_list = get_hints(country, amount, cursor=cursor)
    print(hints_list)
    hints = []
    born_count, died_count, rests_count = len(hints_list["born"]), len(hints_list["died"]), \
                                            len(hints_list["rests"])
    if born_count > 0:
        i = 0
        for hint in hints_list["born"]:
            hints.append(hint)
            i += 1
            cond_a, cond_b = i >= amount, (i >= (amount - 1) and died_count > 0)
            if cond_a or cond_b:
                break
    if died_count and len(hints) < amount:
        i = 0
        for hint in hints_list["died"]:
            hints.append(hint)
            i += 1
            if i >= amount:
                break
    if rests_count and len(hints) < amount:
        i = 0
        for hint in hints_list["rests"]:
            hints.append(hint)
            i += 1
            if i >= amount:
                break
    if len(hints) == 0:
        return json.dumps(["No Available Hint"])
    print(hints)
    return json.dumps(hints)


@app.route('/get_country')
def get_random_country():
    user = request.args.get(GAME_PARAMETERS["user"])
    query = f"SELECT location FROM globalinfoapp.locations WHERE id NOT IN " \
            f"(SELECT location FROM game_locations WHERE gid=(SELECT id FROM games WHERE uid={user} LIMIT 1)) " \
            f"ORDER BY RAND() LIMIT 1;"
    # query = "SELECT location FROM locations ORDER BY RAND() LIMIT 1"
    try:
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute(query)
        country = cursor.fetchone()
        print(country)
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
        db = mysql.connect()
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
    rests_query = f"SELECT DISTINCT name,latitude,longitude FROM restaurants WHERE city_id=" \
                  f"(SELECT id FROM locations WHERE location='{country}');"
    rests_count_query = f"SELECT COUNT(name) FROM restaurants WHERE city_id=" \
                        f"(SELECT id FROM locations WHERE location='{country}');"
    try:
        db = mysql.connect()
        cursor = db.cursor()
        # print("cursor1", cursor)
        cursor.execute(born_query)
        born_country = cursor.fetchall()
        born_country = [x[0] for x in born_country]
        cursor.execute(died_query)
        died_country = cursor.fetchall()
        died_country = [x[0] for x in died_country]
        cursor.execute(rests_query)
        rests_country = cursor.fetchall()
        rests_country = list(rests_country)
        for x in range(len(rests_country)):
            rests_country[x] = list(rests_country[x])
            (rests_country[x])[1] = str((rests_country[x])[1])
            (rests_country[x])[2] = str((rests_country[x])[2])
        rests_country = [":".join(x) for x in rests_country]

        cursor.execute(rests_count_query)
        rests_count = cursor.fetchall()
        rests_count = [x[0] for x in rests_count]

        b = ",".join(born_country)
        d = ",".join(died_country)
        r = ",".join(rests_country)
        ret = {"born": b, "died": d, "rests": r, "restsCount": rests_count}
        return json.dumps(ret)
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/users', methods=['GET', 'POST'], )
def users():
    username, psw = request.args.get('user'), request.args.get('pass')
    uid, is_admin = -1, False
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    if request.method == 'POST':
        gender, age = request.args.get('gender'), request.args.get('age')
        if not gender:
            gender = ''
        if not age:
            age = "1970-01-01"
        query = f"INSERT INTO users (username, password, age, gender) VALUES " \
                     f"('{username}', '{psw}', '{age}', '{gender}');"
        insert_query(db=db, query=query, cursor=cursor)
        query = f"SELECT id FROM users WHERE (username='{username}' AND password='{psw}') LIMIT 1;"
        cursor.execute(query)
        record = cursor.fetchone()
        if record:
            uid = record[0]
    else:
        try:
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
    ret_value = {"score": None, "letters": None, "curr_country": None, "strikes": None, "gid": None, "hints": None}
    try:
        db = mysql.connect()
        cursor = db.cursor()
        query = f"SELECT id, current_score, strikes, hints, current_location FROM games WHERE uid='{user}';"
        rows = cursor.execute(query)
        game_record = cursor.fetchone()
        if not game_record:
            return json.dumps(None)
        ret_value["gid"], ret_value["score"], ret_value["strikes"], ret_value["hints"], ret_value["curr_country"] = \
            game_record
        ret_value["curr_country"] = id_to_country(cursor=cursor, country_id=ret_value["curr_country"])
        game_id = ret_value["gid"]
        query = f"SELECT letter FROM game_letter WHERE gid={game_id}"
        cursor.execute(query)
        letters_records = cursor.fetchall()
        if letters_records:
            letters = [letter[0] for letter in letters_records]
            ret_value["letters"] = ",".join(letters)
    except Exception as e:
        print(e)
        return DatabaseError(e)
    return json.dumps(ret_value)


@app.route('/gameover')
def delete_game():
    game_id = request.args.get(GAME_PARAMETERS["game"])
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return DatabaseError(e)
    rows = letters_query = f"DELETE FROM game_letter WHERE gid={game_id}"
    delete_query(query=letters_query, db=db, cursor=cursor, to_commit=False)
    locations_query = f"DELETE FROM game_locations WHERE gid={game_id}"
    rows = delete_query(query=locations_query, db=db, cursor=cursor)
    game_query = f"DELETE FROM games WHERE id={game_id}"
    rows = delete_query(query=game_query, db=db, cursor=cursor)
    return str(rows)


@app.route('/user_country')
def users_countries():
    uid = request.args.get('uid')
    country_range = request.args.get('range')
    fail = {"result": False, "data": "Database Connection lost"}
    if not uid:
        return json.dumps(fail)
    if country_range:
        country_range = country_range.split(",")
        start_range, end_range = int(country_range[0]), int(country_range[1])
        min_range, max_range = min(start_range, end_range),  max(start_range, end_range)
    else:
        min_range, max_range = 0, 50
    ret = {"count": None, "locations": None}
    try:
        db = mysql.connect()
        cursor = db.cursor()
        is_admin = check_if_admin(uid, cursor=cursor)
        if is_admin:
            max_id = count_records(cursor=cursor, table="locations")
            max_range = min(max_range, max_id)
            query = f"SELECT location FROM locations WHERE id BETWEEN {min_range} AND {max_range};"
        else:
            max_id = count_records(table="user_locations", where=f"uid={uid}", cursor=cursor)
            if max_id < 0:
                return json.dumps(fail)

            if max_id < min_range:
                max_range = max_id
                min_range = 0
            query = f"SELECT location FROM locations WHERE id IN (SELECT location FROM user_locations WHERE uid={uid}) " \
                    f"LIMIT {min_range}, {max_range};"
        ret["count"] = max_id
        print(query)
        rows = cursor.execute(query)
        records = cursor.fetchall()
        if records:
            places = [x[0] for x in records if x[0] != '']
            locations = ",".join(places)
            ret["locations"] = locations
        return json.dumps(ret)
    except Exception as e:
        print(e)
        pass
    return json.dumps(fail)


@app.route('/savegame', methods=['POST'])
def save_game():
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    parameters = GAME_PARAMETERS
    args = request.form
    curr_location, countries, letters, strikes, score, user, hints = \
        parameters["curr_country"], parameters["countries"], parameters["letters"], \
        parameters["strikes"], parameters["score"], parameters["user"], parameters["hints"]

    curr_location, countries, letters, strikes, score, user, hints = \
        args[curr_location], args[countries], args[letters], args[strikes], args[score], args[user], args[hints]

    # print(curr_location, countries, letters, strikes, score, user)
    if str(curr_location) != "0":
        curr_location = country_to_id(country=curr_location, cursor=cursor)
    else:
        curr_location = "NULL"
    # print("curr location", curr_location)
    get_query = f"SELECT id FROM games WHERE uid={user};"
    cursor.execute(get_query)
    game_record = cursor.fetchone()
    game_exists, game_id = False, -1
    # print(game_record)
    if game_record:
        game_exists = True
        game_id = game_record[0]
    if not game_exists:
        hints = max(0,3-int(hints))
        game_query = f"INSERT INTO games (uid, current_score, strikes, hints, current_location) VALUES " \
                f"({user}, {score}, {strikes}, {hints}, {curr_location});"
        insert_rows = insert_query(db=db, query=game_query, cursor=cursor)
    else:
        game_query = f"UPDATE games SET current_score = {score}, strikes = {strikes}," \
                f"current_location = {curr_location} WHERE uid={user};"
        update_rows = update_query(query=game_query, db=db, cursor=cursor)
        update_hints(db=db, uid=user, amount=hints, relative_amount=True, cursor=cursor)
        delete_letters = f"DELETE FROM game_letter WHERE gid={game_id};"
        rows = delete_query(query=delete_letters, db=db, cursor=cursor)
    if not game_exists:
        cursor.execute(get_query)
        game_record = cursor.fetchone()
        game_id = game_record[0]
    # insert letters and locations
    # letters_arr, locations = letters.split(","), countries.split(",")
    letters_arr = letters.split(",") if letters != "" else []
    locations = countries.split(",") if countries != "" else []
    letters_arr = [(game_id, letter) for letter in letters_arr]
    try:
        if len(letters_arr) > 0:
            query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
            insert_query(db=db, query=query, execmany=letters_arr, cursor=cursor)
            # cursor.executemany(query, letters_arr)
        if len(locations) > 0:
            locations_idx = countries_to_ids(locations, cursor=cursor)
            locations = [(game_id, location) for location in locations_idx if location is not None]
            query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
            # cursor.executemany(query, locations)
            insert_query(db=db, query=query, execmany=locations, cursor=cursor)
            is_admin = check_if_admin(user, cursor=cursor)
            if not is_admin:
                user_locations = filter_countries(locations_idx, user, cursor=cursor)
                if len(user_locations) > 0:
                    query = f"INSERT INTO user_locations (uid, location) VALUES (%s, %s)"
                    locations = [(user, location) for location in user_locations if location is not None]
                    insert_query(db=db, query=query, execmany=locations, cursor=cursor)
                # cursor.executemany(query, locations)
        # db.commit()
    except Exception as e:
        print(e)
        return DatabaseError(e)
    return str(game_id)


@app.route('/update_hints')
def use_hint():
    uid, hints = request.args.get("user"), request.args.get("hints")
    if not hints:
        hints = -1
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    t = update_hints(db=db, uid=uid, amount=hints, relative_amount=True, cursor=cursor)
    return str(t)


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
            db = mysql.connect()
            cursor = db.cursor()
            ret_val = update_query(db=db, query=query, cursor=cursor)
            # ret_val = cursor.execute(query)
            # db.commit()
        except Exception as e:
            print(e)
            pass
        return str(ret_val)
    else:
        query = f"SELECT username, password, age, gender FROM users WHERE users.id = {request.args.get('uid')};"
        try:
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                return {}
            return json.dumps(result[0], default=str)
        except Exception as e:
            print(e)
            return DatabaseError(e)


@app.route('/get_genres')
def get_all_genres():
    query = "SELECT genre FROM genres"
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    records = select_query(query=query, is_many=True, cursor=cursor)
    if records:
        records = [x[0] for x in records]
    return json.dumps(records)


@app.route('/add_person', methods=['POST'])
def add_person():
    arg = request.json
    keys = arg.keys()
    try:
        db = mysql.connect()
        cursor = db.cursor()
    except Exception as e:
        print("problem connecting", e)
        return "500"
    name = arg["name"] if "name" in keys else ''
    if name == '':
        return "-1"
    does_exist = select_query(query=f"SELECT id FROM people_info WHERE name='{name}'", is_many=False, cursor=cursor)
    print(does_exist)
    if not does_exist:
        bornin = arg['bornin'] if 'bornin' in keys else None
        diedin = arg['diedin'] if 'diedin' in keys else None
        gender = arg['gender'] if 'gender' in keys else 'f'
        if not (bornin or diedin):
            return "-1"
        # insert to people_info
        born = add_location(bornin, db=db) if bornin else "NULL"
        died = add_location(diedin, db=db) if bornin else "NULL"
        if bornin and diedin:
            person_query = f"INSERT INTO people_info (name, gender, BornIn, DiedIn) VALUES ('{name}', '{gender}', " \
                           f"{born}, {died});"
        elif bornin:  # if only born in
            person_query = f"INSERT INTO people_info (name, gender, BornIn) VALUES ('{name}', '{gender}', " \
                           f"{born});"
        else:  # if only died in
            person_query = f"INSERT INTO people_info (name, gender, DiedIn) VALUES ('{name}', '{gender}', " \
                           f"{died});"
        pid = -1
        try:
            rows = insert_query(db=db, query=person_query, cursor=cursor)
            pid = cursor.lastrowid
        except Exception as e:
            return DatabaseError(e)
    else:
        pid = does_exist[0]
    # no movie to add, se we're done
    movie = arg["movie"] if "movie" in keys else ''
    if movie == '':
        return str(pid)
    job = arg["job"] if "job" in keys else '0'
    genres = arg["genres"] if "genres" in keys else ''
    # add movie
    movie_query = f"INSERT INTO movies (movieName) VALUES ('{movie}')"
    rows = insert_query(db=db, query=movie_query, cursor=cursor)
    if rows < 1:
        return "-1"
    movie_id = cursor.lastrowid
    # add person movie
    if not job:
        job = '0'  # actor by default
    if movie_id > 0:
        query = f"INSERT INTO people_movies (pid, movieId, job_id) VALUES ({pid}, {movie_id}, {job});"
        rows = insert_query(db=db, query=query, cursor=cursor)
    # if movie has no genres, return person's id
    if not genres:
        return str(pid)
    if len(genres) <=0:
        return str(pid)
    # add genres
    # genres = [genres list]
    genres_str = ", ".join([f"'{g}'" for g in genres])
    query = f"SELECT id FROM genres WHERE genre IN ({genres_str});"
    genres_ids = select_query(query=query, cursor=cursor, is_many=True)
    if genres_ids:
        genres_values = [(movie_id, g) for g in genres_ids]
        insert = f"INSERT INTO movies_genres (movieId, genreId) VALUES (%s, %s)"
        rows = insert_query(query=insert, db=db, cursor=cursor, execmany=genres_values)
    return str(pid)


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


app.run(debug=True, port=PORT)

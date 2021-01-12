from server_helper import *


@app.route('/bestScores')
def get_best_scores():
    """

    :return: error if failed, best scores if succeeded
    """
    cursor = None
    try:
        cursor = db.cursor()
        query_best_10_scores = "SELECT users.username, score_history.score, score_history.datetime FROM " \
                               "score_history, users WHERE score_history.uid=users.id ORDER BY score " \
                               "DESC LIMIT 10;"
        cursor.execute(query_best_10_scores)
        result = cursor.fetchall()
        cursor.close()  # close resource
        return json.dumps(result, default=datetime_tostring)  # return best scores
    except Exception as e:  # failed
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/admin/best_score')
def get_best_score():
    """
    function returns the best score of the game
    """
    cursor = None
    try:
        cursor = db.cursor()
        best_score_query = "SELECT username, score, datetime FROM users, (SELECT uid, MAX(score) AS " \
                           "score, datetime FROM score_history) AS best_score WHERE users.id = " \
                           "best_score.uid;"
        cursor.execute(best_score_query)
        result = cursor.fetchall()  # get record
        cursor.close()  # close resources
        if len(result) == 1:  # if there's results
            message = f"{result[0][0]} has the highest score which is {result[0][1]} since {result[0][2]}.\n"
            return message
        else:  # no results
            return "0 games were ended"
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/admin/quantity_of_gamers')
def get_number_of_gamers():
    cursor = None
    try:
        cursor = db.cursor()
        num_gamers_query = "SELECT COUNT(*) FROM ((SELECT uid FROM games) UNION (SELECT uid FROM " \
                           "score_history)) AS all_gamers;"
        cursor.execute(num_gamers_query)
        result = cursor.fetchone()
        cursor.close()
        message = f"Number of people playing by far: {result[0]}\n"

        return message
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/admin/age_statistics')
def get_age_statistics():
    cursor = None
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
        hundred_years_ago = datetime.date.today() - relativedelta(years=120)
        cursor.execute(query_avg_score_according_to_ages, (hundred_years_ago, fifty_five_years_ago))
        avg_score_elders = cursor.fetchall()[0][0]
        avg_score_young = 0 if avg_score_young is None else avg_score_young
        avg_score_adults = 0 if avg_score_adults is None else avg_score_adults
        avg_score_elders = 0 if avg_score_elders is None else avg_score_elders
        message = f"Average score for ages 0-25: {avg_score_young}\nAverage score for ages 26-55: " \
                  f"{avg_score_adults}\nAverage score for ages 56-120: {avg_score_elders}\n"
        cursor.close()
        return message
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/admin/gender')
def get_gender_statistics():
    cursor = None
    try:
        query_gender_score_sum = "SELECT SUM(score) FROM users, score_history WHERE users.id = score_history.uid " \
                                 "AND users.gender = %s;"
        cursor = db.cursor()
        cursor.execute(query_gender_score_sum, ('m', ))
        male_sum = cursor.fetchall()[0][0]
        male_sum = 0 if male_sum is None else male_sum
        cursor.execute(query_gender_score_sum, ('f', ))
        female_sum = cursor.fetchall()[0][0]
        female_sum = 0 if female_sum is None else female_sum
        message = f"Cumulative score for males: {male_sum}\nCumulative score for females: {female_sum}\n"
        cursor.close()
        return message
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/hint')
def server_hints():
    """
    get hints
    :return: hints
    """
    country, user = request.args.get('country'), request.args.get('user')
    is_new = request.args.get("new")  # if a new game
    fail = {"result": False, "data": "Database Connection lost"}
    if not (user or country):  # invalid input
        fail["data"] = "invalid input"
        return fail
    try:
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    if not is_new:  # if an existing game
        hints_query = f"SELECT hints FROM games WHERE uid={user}"
        hints = select_query(query=hints_query, is_many=False, cursor=cursor)  # get number of hints
        if not hints:
            fail["data"] = "[No Available Hint]"
            return fail
        amount = hints[0]
    else:  # if new game - get 3 hints
        amount = 3
    country = country_to_id(cursor=cursor, country=country)
    if amount < 1:  # no available hints
        cursor.close()
        return "No Available Hint"

    hints_list = get_hints(country, amount, cursor=cursor)  # get hints
    hints = []
    born_count, died_count, rests_count = len(hints_list["born"]), len(hints_list["died"]), \
                                            len(hints_list["rests"])  # get how many hints of each type
    if born_count > 0:  # if there are born locations
        i = 0
        for hint in hints_list["born"]:
            hints.append(hint)
            i += 1
            cond_a, cond_b = i >= amount, (i >= (amount - 1) and died_count > 0)  # if we can use died hint
            if cond_a or cond_b:
                break
    if died_count and len(hints) < amount:   # if there are died locations, and needed more hints
        i = 0
        for hint in hints_list["died"]:
            hints.append(hint)
            i += 1
            if i >= amount:
                break
    if rests_count and len(hints) < amount:  # if we need more hints, and there are available
        i = 0
        for hint in hints_list["rests"]:
            hints.append(hint)
            i += 1
            if i >= amount:
                break
    if len(hints) == 0:
        return json.dumps(["No Available Hint"])
    cursor.close()
    return json.dumps(hints)


@app.route('/get_country')
def get_random_country(user=None):
    """
    :param user: user id - from new game
    :return: a random country the user didnt visit
    """
    if not user:
        user = request.args.get(GAME_PARAMETERS["user"])
    query = f"SELECT location FROM locations WHERE id NOT IN " \
            f"(SELECT location FROM game_locations WHERE gid=(SELECT id FROM games WHERE uid={user} LIMIT 1)) " \
            f"ORDER BY RAND() LIMIT 1;"
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(query)
        country = cursor.fetchone()
        cursor.close()
        if len(country) > 0:
            return country[0]
        return "fail"
    except Exception as e:
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/movies')
def get_person_movies():
    person = request.args.get('person')
    ret = {"gender": "", "actedIn": [], "directed": []}
    cursor = None
    if not person:  # if there is not person to get data about
        return json.dumps(None)
    try:
        cursor = db.cursor()
        # get person gender and id
        query = f"SELECT id, gender FROM people_info WHERE Name='{person}' LIMIT 1"
        cursor.execute(query)
        record = cursor.fetchone()
        if not record:
            cursor.close()
            return json.dumps(None)
        pid, ret["gender"] = record
        # get all his/her movies
        query = f"SELECT movieId, job_id FROM people_movies WHERE pid={pid}"
        cursor.execute(query)
        record = cursor.fetchall()  # ((301,0/1), (555,0/1),...)
        if not record:
            cursor.close()
            return json.dumps(None)
        # check for directed movies and acted movies
        actor_id, directors_id = "00", "01"
        actor_movies = tuple((x[0]) for x in record if actor_id in str(x[1]))
        director_movies = tuple(str(x[0]) for x in record if directors_id in str(x[1]))
        # get person movies by [{movie:[genres]},...]
        if len(actor_movies) > 0:
            ret["actedIn"] = movies_record_to_list(movies_idx=actor_movies, cursor=cursor)
        if len(director_movies) > 0:
            ret["directed"] = movies_record_to_list(movies_idx=director_movies, cursor=cursor)
        cursor.close()
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)
    return json.dumps(ret)


@app.route('/get_people')
def get_all_related():
    # setup queries
    country, cursor = request.args.get('country'), None
    born_query = f"SELECT Name FROM people_info WHERE BornIn IN " \
                 f"(SELECT id FROM locations WHERE location='{country}');"
    died_query = f"SELECT Name FROM people_info WHERE DiedIn IN " \
                 f"(SELECT id FROM locations WHERE location='{country}');"
    rests_query = f"SELECT DISTINCT name,latitude,longitude,url FROM restaurants WHERE city_id IN" \
                  f"(SELECT id FROM locations WHERE location='{country}');"
    try:
        cursor = db.cursor()
        # handle born countries
        cursor.execute(born_query)
        born_country = cursor.fetchall()
        born_country = [x[0] for x in born_country]
        # handle died countries
        cursor.execute(died_query)
        died_country = cursor.fetchall()
        died_country = [x[0] for x in died_country]
        # handle restaurants
        cursor.execute(rests_query)
        rests_country = cursor.fetchall()
        rests_country = list(rests_country)
        rests_count = [len(rests_country)]
        # get restaurants name, location and url
        for x in range(len(rests_country)):
            rests_country[x] = list(rests_country[x])
            (rests_country[x])[1] = str((rests_country[x])[1])
            (rests_country[x])[2] = str((rests_country[x])[2])
            (rests_country[x])[3] = str((rests_country[x])[3])
        rests_country = [";".join(x) for x in rests_country]
        b = ",".join(born_country)
        d = ",".join(died_country)
        r = ",".join(rests_country)
        ret = {"born": b, "died": d, "rests": r, "restsCount": rests_count}
        cursor.close()
        return json.dumps(ret)
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)


@app.route('/users', methods=['GET', 'POST'], )
def users():
    """
    POST function to register, GET function for login, to get user id and if admin
    :return: user id and if admin
    """
    username, psw = request.args.get('user'), request.args.get('pass')
    uid, is_admin = -1, False  # default values
    try:
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    if request.method == 'POST':
        gender, age = request.args.get('gender'), request.args.get('age')
        # check if username exists
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        rows_returned = len(cursor.fetchall())
        if rows_returned > 0:
            cursor.close()
            return json.dumps(["username already exists! please try a different one and try again!"])
        # username does not exist
        query = f"INSERT INTO users (username, password, age, gender) VALUES " \
                     f"('{username}', '{psw}', '{age}', '{gender}');"
        val = insert_query(query=query, cursor=cursor)
        if val < 1:  # if failed to insert
            cursor.close()
            return json.dumps(["Please check that your username is no longer than 20 characters and password is no "
                               "longer than 25 characters.Then, please try again!"])
        query = f"SELECT id FROM users WHERE (username='{username}' AND password='{psw}') LIMIT 1;"
        cursor.execute(query)
        record = cursor.fetchone()
        if record:
            uid = record[0]
    else:  # GET function
        try:
            query = f"SELECT id FROM users WHERE (username='{username}' AND password='{psw}') LIMIT 1;"
            cursor.execute(query)
            record = cursor.fetchone()
            if record:  # if found user
                uid = record[0]
                r = check_if_admin(uid, cursor=cursor)
                if r:
                    is_admin = True
        except Exception as e:
            print("e", e)
    if cursor:
        cursor.close()
    return json.dumps({"uid": uid, "admin": is_admin})


@app.route('/getgame', methods=['GET'])
def get_game():
    """
    :return: ret_value
    """
    user, cursor = request.args.get(GAME_PARAMETERS["user"]), None
    ret_value = {"score": None, "letters": None, "curr_country": None, "strikes": None, "gid": None, "hints": None}
    try:
        cursor = db.cursor()
        query = f"SELECT id, current_score, strikes, hints, current_location FROM games WHERE uid='{user}';"
        rows = cursor.execute(query)  # get game relevant values
        game_record = cursor.fetchone()
        if not game_record:  # if failed to get game
            cursor.close()
            return json.dumps(None)
        # dump game_record values
        ret_value["gid"], ret_value["score"], ret_value["strikes"], ret_value["hints"], ret_value["curr_country"] = \
            game_record
        # get current country id
        ret_value["curr_country"] = id_to_country(cursor=cursor, country_id=ret_value["curr_country"])
        game_id = ret_value["gid"]
        # get game letters
        query = f"SELECT letter FROM game_letter WHERE gid={game_id}"
        cursor.execute(query)
        letters_records = cursor.fetchall()
        if letters_records:
            letters = [letter[0] for letter in letters_records]
            ret_value["letters"] = ",".join(letters)
        cursor.close()  # close resources
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)
    return json.dumps(ret_value)


@app.route('/gameover')
def delete_game(game_id=None):
    """

    :param game_id: game id, for newgame use
    :return: if succeeded to delete game
    """
    if not game_id:  # if from client
        game_id = request.args.get(GAME_PARAMETERS["game"])
    try:
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return DatabaseError(e)
    count = count_records("games", cursor=cursor, where=f"id={game_id}")  # get game
    if count < 1:  # if there is not game
        return -1
    # delete game letters
    letters_query = f"DELETE FROM game_letter WHERE gid={game_id}"
    rows = delete_query(query=letters_query, cursor=cursor, to_commit=False)
    if rows < 0:  # failed delete
        return -1
    # delete game locations
    locations_query = f"DELETE FROM game_locations WHERE gid={game_id}"
    rows = delete_query(query=locations_query, cursor=cursor)
    if rows < 0:  # failed delete
        return -1
    # save score in score_history
    score_query = f"SELECT uid, current_score FROM games WHERE id={game_id}"
    score = select_query(query=score_query, cursor=cursor, is_many=False)
    if score:
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        score_query = f"INSERT INTO score_history (uid, score, datetime) VALUES " \
                      f"({score[0]}, {score[1]}, '{dt_string}'); "
        rows = insert_query(query=score_query, cursor=cursor)
    # delete game
    game_query = f"DELETE FROM games WHERE id={game_id}"
    rows = delete_query(query=game_query, cursor=cursor)
    cursor.close()
    if rows < 0:  # failed delete
        return "-1"
    return str(rows)


@app.route('/user_country')
def users_countries():
    """
    :return: all user saved locations
    """
    uid, cursor = request.args.get('uid'), None
    country_range = request.args.get('range')
    fail = {"result": False, "data": "Database Connection lost"}
    if not uid:  # if invalid input
        return json.dumps(fail)
    if country_range:  # if there's a range - make sure it's legal, and set local variables
        country_range = country_range.split(",")
        start_range, end_range = int(country_range[0]), int(country_range[1])
        min_range, max_range = min(start_range, end_range),  max(start_range, end_range)
    else:  # if no range - default range is the first 50
        min_range, max_range = 0, 50
    ret = {"count": None, "locations": None}
    try:
        cursor = db.cursor()
        is_admin = check_if_admin(uid, cursor=cursor)
        # handle max range and max_id - max id that we want to get from locations
        if is_admin:
            max_id = count_records(cursor=cursor, table="locations")  # get number of locations in general
            max_range = min(max_range, max_id)  #
            query = f"SELECT location FROM locations WHERE id BETWEEN {min_range} AND {max_range};"
        else:
            max_id = count_records(table="user_locations", where=f"uid={uid}", cursor=cursor)
            if max_id < 0:  # if failed to count
                cursor.close()
                return json.dumps(fail)

            if max_id < min_range:  # if range is below min_range - get first max_id
                max_range = max_id
                min_range = 0
            query = f"SELECT location FROM locations WHERE id IN (SELECT location FROM user_locations " \
                    f"WHERE uid={uid}) LIMIT {min_range}, {max_range};"
        ret["count"] = max_id  # count how many locations the user has
        rows = cursor.execute(query)  # get locations
        records = cursor.fetchall()
        if records:  # if there are locations
            places = [x[0] for x in records if x[0] != '']
            locations = ",".join(places)
            ret["locations"] = locations
        cursor.close()
        return json.dumps(ret)
    except Exception as e:
        print(e)
    if cursor:
        cursor.close()
    return json.dumps(fail)


@app.route('/newgame')
def new_game():
    """
    function deletes old game (if exists) and returns a random country
    :return: random location
    """
    uid = request.args.get("uid")
    fail = {"result": False, "data": "Invalid Input"}
    if not uid:  # if we didn't recieve uid - we cant make a new game
        return json.dumps(fail)
    query = f"SELECT id FROM games WHERE uid={uid}"
    gid = select_query(query, is_many=False)
    if gid:  # if there is a game
        delete_game(gid[0])
    country = get_random_country(uid)
    return country


@app.route('/savegame', methods=['POST'])
def save_game():
    """
    POST function - save game
    :return: game id
    """
    try:
        cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    parameters = GAME_PARAMETERS
    # get parameters
    args = request.form
    curr_location, countries, letters, strikes, score, user, hints = \
        parameters["curr_country"], parameters["countries"], parameters["letters"], \
        parameters["strikes"], parameters["score"], parameters["user"], parameters["hints"]

    curr_location, countries, letters, strikes, score, user, hints = \
        args[curr_location], args[countries], args[letters], args[strikes], args[score], args[user], args[hints]

    if str(curr_location) != "0":  # if country - get its id
        curr_location = country_to_id(country=curr_location, cursor=cursor)
    else:  # no country - insert null
        curr_location = "NULL"
    get_query = f"SELECT id FROM games WHERE uid={user};"  # get game id
    cursor.execute(get_query)
    game_record = cursor.fetchone()
    game_exists, game_id = False, -1

    if game_record:  # if found game - games exists, anf set game_id
        game_exists = True
        game_id = game_record[0]
    if not game_exists:  # if game not found - its a new game
        hints = max(0, 3-int(hints))
        game_query = f"INSERT INTO games (uid, current_score, strikes, hints, current_location) VALUES " \
                f"({user}, {score}, {strikes}, {hints}, {curr_location});"
        insert_rows = insert_query(query=game_query, cursor=cursor)
    else:  # if game exists -  we want to update it
        game_query = f"UPDATE games SET current_score = {score}, strikes = {strikes}," \
                f"current_location = {curr_location} WHERE uid={user};"
        update_rows = update_query(query=game_query, cursor=cursor)  # update game
        update_hints(uid=user, amount=hints, relative_amount=True, cursor=cursor)  # update hints
        delete_letters = f"DELETE FROM game_letter WHERE gid={game_id};"  # delete all letters
        rows = delete_query(query=delete_letters, cursor=cursor)
    if not game_exists:  # if game didn't exist - it exists now, and we want it's id
        cursor.execute(get_query)
        game_record = cursor.fetchone()
        game_id = game_record[0]
    # insert letters and locations
    # setup letters and locations
    letters_arr = letters.split(",") if letters != "" else []
    locations = countries.split(",") if countries != "" else []
    letters_arr = [(game_id, letter) for letter in letters_arr]
    try:
        if len(letters_arr) > 0:  # insert letters
            query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
            insert_query(query=query, execmany=letters_arr, cursor=cursor)
            # cursor.executemany(query, letters_arr)
        if len(locations) > 0:  # insert game locations and user locations
            locations_idx = countries_to_ids(locations, cursor=cursor)
            locations = [(game_id, location) for location in locations_idx if location is not None]
            query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
            # cursor.executemany(query, locations)
            insert_query(query=query, execmany=locations, cursor=cursor)
            is_admin = check_if_admin(user, cursor=cursor)
            if not is_admin:  # if admin - we don't need to save it's visited locations
                # get all new locations
                user_locations = filter_countries(locations_idx, user, cursor=cursor)
                if len(user_locations) > 0:  # if there's a new location
                    query = f"INSERT INTO user_locations (uid, location) VALUES (%s, %s)"
                    locations = [(user, location) for location in user_locations if location is not None]
                    insert_query(query=query, execmany=locations, cursor=cursor)
        if cursor:
            cursor.close()
    except Exception as e:
        print(e)
        if cursor:
            cursor.close()
        return DatabaseError(e)
    return str(game_id)


@app.route('/update_hints')
def use_hint():
    """
    function updates hints for user by hints amount
    """
    uid, hints = request.args.get("user"), request.args.get("hints")
    if not hints:
        hints = -1
    t = update_hints(uid=uid, amount=hints, relative_amount=True)
    return str(t)


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    """
    POST for updating user, GET for getting details
    requires uid, and username to change username, pass to change password
    """
    global db
    cursor = None
    if request.method == 'POST':
        # get params
        username, psw, uid = request.args.get("username"), request.args.get("pass"), request.args.get("uid")
        ret_val = -1
        # create query by params
        if username and psw:  # update username and password
            query = f"UPDATE users SET username = '{username}', password = '{psw}' WHERE id={uid};"
        elif username:  # update username
            query = f"UPDATE users SET username = '{username}' WHERE id={uid};"
        elif psw:
            query = f"UPDATE users SET password = '{psw}' WHERE id={uid};"
        else:  # no values to update
            return str(ret_val)
        try:  # update
            cursor = db.cursor()
            ret_val = update_query(query=query, cursor=cursor)
        except Exception as e:  # failed connecting
            print(e)
        if cursor:
            cursor.close()
        return str(ret_val)
    else:  # GET call - get user details
        query = f"SELECT username, password, age, gender FROM users WHERE users.id = {request.args.get('uid')};"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if cursor:
                cursor.close()
            if len(result) == 0:
                return {}
            return json.dumps(result[0], default=str)
        except Exception as e:
            print(e)
            if cursor:
                cursor.close()
            return DatabaseError(e)


@app.route('/get_genres')
def get_all_genres():
    """
    :return: all genres strings from db
    """
    query = "SELECT DISTINCT genre FROM genres"
    records = select_query(query=query, is_many=True)
    if records:
        records = [x[0] for x in records]
    return json.dumps(records)


@app.route('/add_person', methods=['POST'])
def add_person():
    """
    function adds a person to DB
    """
    arg = request.json
    keys = arg.keys()
    try:
        cursor = db.cursor()
    except Exception as e:  # connection problems
        print("problem connecting", e)
        return json.dumps([500])
    name = arg["name"] if "name" in keys else ''  # get name
    if name == '':  # if there's no name - invalid input
        if cursor:
            cursor.close()
        return json.dumps(["Name of personality was not given"])
    # check if name exists
    does_exist = select_query(query=f"SELECT id FROM people_info WHERE name='{name}'",
                              is_many=False, cursor=cursor)
    if not does_exist:  # if person doesn't exist
        # get parameters
        bornin = arg['bornin'] if 'bornin' in keys else None
        diedin = arg['diedin'] if 'diedin' in keys else None
        gender = arg['gender'] if 'gender' in keys else 'f'
        if not (bornin or diedin):  # if not locations, invalid input
            if cursor:
                cursor.close()
            return json.dumps(["At least one location must be given!<br>After inserting the data please try again!"])
        # insert to people_info
        born = add_location(bornin, cursor=cursor) if bornin else "NULL"
        died = add_location(diedin, cursor=cursor) if bornin else "NULL"
        # set query according to input
        if bornin and diedin:
            person_query = f"INSERT INTO people_info (name, gender, BornIn, DiedIn) VALUES ('{name}', '{gender}', " \
                           f"{born}, {died});"
        elif bornin:  # if only born in
            person_query = f"INSERT INTO people_info (name, gender, BornIn) VALUES ('{name}', '{gender}', " \
                           f"{born});"
        else:  # if only died in
            person_query = f"INSERT INTO people_info (name, gender, DiedIn) VALUES ('{name}', '{gender}', " \
                           f"{died});"
        try:  # insert person
            rows = insert_query(query=person_query, cursor=cursor)
            if rows == 0:
                json.dumps(["The given data was not updated!<br>Please check that the number of characters in name "
                            "and city is no longer than 70.<br>Then please try again!"])
            pid = cursor.lastrowid  # get person id
        except Exception as e:
            if cursor:
                cursor.close()
            return json.dumps([500])
    else:  # if person exists in db - we dont want to add it, but it's details
        pid = does_exist[0]  # person id

    movie = arg["movie"] if "movie" in keys else ''
    if movie == '':  # no movie to add, se we're done
        if cursor:
            cursor.close()
        return json.dumps(["The data on the personality was successfully saved!<br>Nothing related the movie was "
                           "added."])
    # get movies parameters
    job = arg["job"] if "job" in keys else '0'  # actor is default job
    genres = arg["genres"] if "genres" in keys else ''
    # add movie
    movie_query = f"INSERT INTO movies (movieName) VALUES ('{movie}')"
    rows = insert_query(query=movie_query, cursor=cursor)
    if rows < 1:  # if failed inserting
        if cursor:
            cursor.close()
        return json.dumps(["The name of the movie is too long, please check that the length is smaller then 105 "
                           "characters"])
    movie_id = cursor.lastrowid  # get movie id
    # add person movie
    if not job:
        job = '0'  # actor by default
    if movie_id > 0:
        query = f"INSERT INTO people_movies (pid, movieId, job_id) VALUES ({pid}, {movie_id}, {job});"
        rows = insert_query(query=query, cursor=cursor)
    # if movie has no genres, return person's id
    if not genres:  # not genres
        if cursor:
            cursor.close()
        return json.dumps(["The given data was successfully saved!"])
    if len(genres) <= 0:  # no genres
        if cursor:
            cursor.close()
        return json.dumps(["The given data was successfully saved!"])
    # add genres
    # genres = [genres list]
    genres_str = ", ".join([f"'{g}'" for g in genres])  # setup genres to query
    query = f"SELECT id FROM genres WHERE genre IN ({genres_str});"
    # get all movie genres id for insertion
    genres_ids = select_query(query=query, cursor=cursor, is_many=True)
    if genres_ids:  # if found genres id
        genres_values = [(movie_id, g) for g in genres_ids]
        insert = f"INSERT INTO movies_genres (movieId, genreId) VALUES (%s, %s)"
        rows = insert_query(query=insert, cursor=cursor, execmany=genres_values)
        if cursor:
            cursor.close()
        if rows > 0:
            return json.dumps(["The given data was successfully saved!"])
        else:
            return json.dumps(["Something went wrong with inserting the genres, please try again!"])
    if cursor:
        cursor.close()
    return json.dumps(["Something went wrong with inserting the genres, please try again!"])


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


app.run(debug=True, port=PORT, threaded=False)

from settings import *
from datetime import datetime
import random


def DatabaseError(error):
    return 'Database connection failed', 500


def get_from_option(option, country):
    # query = f"SELECT Name, DiedIn FROM people_info WHERE DiedIn=(SELECT id FROM locations WHERE location='{country} ')"
    if option == 1:
        query = f"SELECT Name, DiedIn FROM people_info WHERE DiedIn='{country} ' ORDER BY RAND() LIMIT 1;"
        keyword = "has died"
    else:
        query = f"SELECT Name, BornIn FROM people_info WHERE BornIn='{country} ' ORDER BY RAND() LIMIT 1;"
        keyword = "was born"
    return query, keyword


@app.route('/hint')
def get_hint():
    options = ["bornin, diedin, restaurant"]
    global i
    print(i)
    i += 1
    try:
        cursor = db.cursor()
        option, country = random.randint(1, 2), request.args.get('country')
        query, keyword = get_from_option(option, country)
        cursor.execute(query)
        result = cursor.fetchall()
        print("result", result)
        if len(result) > 0:
            record = result[0]
            result = f"{record[0]} {keyword} there"
        else:
            query, keyword = get_from_option((option % 2) + 1, country)
            cursor.execute(query)
            result = cursor.fetchone()
            print("result", result)
            if len(result) > 0:
                record = result[0]
                result = f"{record[0]} was {keyword} there"
        return result
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/get_country')
def get_random_country():
    print("random")
    query = "SELECT location FROM locations ORDER BY RAND() LIMIT 1"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        country = cursor.fetchone()
        if len(country) > 0:
            return country[0]
        return "fail"
    except Exception as e:
        return DatabaseError(e)


@app.route('/get_people')
def get_all_related():
    print("get people")
    country = request.args.get('country')
    # born_query = f"SELECT Name FROM people_info WHERE BornIn=(SELECT id FROM locations WHERE location='{country} ');"
    born_query = f"SELECT Name FROM people_info WHERE BornIn='{country} ';"
    # died_query = f"SELECT Name FROM people_info WHERE DiedIn=(SELECT id FROM locations WHERE location='{country} ');"
    died_query = f"SELECT Name FROM people_info WHERE DiedIn='{country} ';"
    try:
        cursor = db.cursor()
        cursor.execute(born_query)
        born_country = cursor.fetchall()
        born_country = [x[0] for x in born_country]
        cursor.execute(died_query)
        died_country = cursor.fetchall()
        died_country = [x[0] for x in died_country]
        print(died_country)
        print("cool")
        b = ",".join(born_country)
        d = ",".join(died_country)
        ret = str(b + "|||" + d)
        print(ret)
        return ret
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/users', methods=['GET', 'POST'], )
def users():
    if request.method == 'POST':
        # add user
        pass
    else:
        try:
            arg1 = request.args.get('user')
            print(arg1)
        except Exception as e:
            print("e", e)
    print('a')
    return redirect('/')


@app.route('/getgame', methods=['GET'])
def get_game():
    parameters, args, cursor = GAME_PARAMETERS, request.args.get, db.cursor()
    curr_location, countries, letters, strikes, score = parameters["curr_country"], parameters["countries"], \
                                                        parameters["letters"], parameters["strikes"], \
                                                        parameters["score"]
    curr_location, countries, letters, strikes, score, user = args(curr_location), args(countries), args(letters), \
                                                              args(strikes), args(score), args(user)


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


def id_to_country(country_id=None):
    if not country_id:
        return None
    query = f"SELECT Location FROM locations WHERE id={country_id}"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        return record[0]
    except Exception as e:
        print(e)
        return None


def country_to_id(country=None):
    if not country:
        return None
    query = f"SELECT id FROM locations WHERE Location='{country}';"
    print(query)
    try:
        cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        return record[0]
    except Exception as e:
        print(e)
        return None


@app.route('/savegame', methods=['POST'])
def save_game():
    parameters, args, cursor = GAME_PARAMETERS, request.args.get, db.cursor()
    curr_location, countries, letters, strikes, score, user = parameters["curr_country"], parameters["countries"], \
                                                        parameters["letters"], parameters["strikes"], \
                                                        parameters["score"], parameters["user"]
    curr_location, countries, letters, strikes, score, user = args(curr_location), args(countries), args(letters), \
                                                        args(strikes), args(score), args(user)
    print(curr_location, countries, letters, strikes, score, user)
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
    if game_exists:
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





@app.route('/', methods=['GET', 'POST'])
def index():
    print("index")
    if request.method == 'POST':
        print(request)
        task_content = request.form['content']
        try:
            cursor = db.cursor()
            return redirect('/')
        except Exception as e:
            print(e)
            return render_template('index.html')
            # return 'There was an issue adding the task'
    else:
        return render_template('index.html')


app.run(debug=True, port=PORT)

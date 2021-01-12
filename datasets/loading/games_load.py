import mysql.connector as mysql


def create_game_table(db, cursor):
    # gid, uid, current_score, strikes
    query = "CREATE TABLE games (id SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
            "uid SMALLINT, FOREIGN KEY(uid) REFERENCES users(id), current_score SMALLINT, " \
            "strikes TINYINT, hints TINYINT, current_location SMALLINT UNSIGNED, FOREIGN KEY(current_location) " \
            "REFERENCES locations(id));"
    try:
        db.commit()
        cursor.execute(query)
        query = f"CREATE TABLE score_history (uid SMALLINT NOT NULL, FOREIGN KEY(uid) REFERENCES users(id), " \
                f"score SMALLINT, datetime DATETIME NOT NULL); "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("Database connection error - creating table")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def letter_table(db, cursor):
    # gid, char
    query = "CREATE TABLE game_letter (gid SMALLINT UNSIGNED NOT NULL, FOREIGN KEY(gid) REFERENCES games(id), " \
            "letter CHAR(1)); "
    try:
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("Database connection error")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def locations_table(db, cursor):
    # gid, location
    try:
        query = "CREATE TABLE game_locations (gid SMALLINT UNSIGNED NOT NULL, FOREIGN KEY(gid) REFERENCES games(id), " \
                "location SMALLINT UNSIGNED, FOREIGN KEY(location) REFERENCES locations(id)); "
        cursor.execute(query)
        db.commit()
        query = "CREATE TABLE user_locations (uid SMALLINT NOT NULL, FOREIGN KEY(uid) REFERENCES users(id), " \
                "location SMALLINT UNSIGNED, FOREIGN KEY(location) REFERENCES locations(id)); "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("Database connection error - creating tables")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def users_table(db, cursor):
    # uid, username, password, age, gender
    try:
        query = f"CREATE TABLE users (id SMALLINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(20)," \
                f"password VARCHAR(25), age DATE, gender CHAR(1)); "
        cursor.execute(query)
        db.commit()
        query = f"CREATE TABLE admins (uid SMALLINT PRIMARY KEY NOT NULL, FOREIGN KEY(uid) REFERENCES users(id)); "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("Database connection error")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def make_users(db, cursor, users):
    records = [user[:-1] for user in users]
    admins = [(user[0],) for user in users if user[-1] == '1']
    users_query = f"INSERT INTO users (id, username, password, age, gender) " \
            f"VALUES(%s, %s, %s, %s, %s)"
    admins_query = f"INSERT INTO admins (uid) VALUES(%s)"
    try:
        cursor.executemany(users_query, records)
        cursor.executemany(admins_query, admins)
        db.commit()
    except mysql.Error as e:
        print("insert users/admin error error")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def create_games(db, cursor, games, game_locations, user_locations, game_letters, score_history):
    # games =  gid, uid, current_score, strikes, current_location, hints
    # locations = gid, location
    # letters = gid, letter
    try:
        query = "INSERT INTO games (id, uid, current_score, strikes, hints, current_location) " \
                "VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.executemany(query, games)
        db.commit()
        query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
        cursor.executemany(query, game_locations)
        query = "INSERT INTO user_locations (uid, location) VALUES (%s, %s);"
        cursor.executemany(query, user_locations)
        query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
        cursor.executemany(query, game_letters)
        db.commit()
        query = "INSERT INTO score_history (uid, score, datetime) VALUES (%s, %s, %s);"
        cursor.executemany(query, score_history)
        db.commit()
    except mysql.Error as e:
        print("Database connection error - loading games data")
        print(e)
        return -1
    except Exception as e:
        print(e)
        exit(5)


def load_file(file_name):
    records = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            line = line.strip().split(",")
            line = [l.strip() for l in line]
            row = tuple(line)
            records.append(row)
    return records


def load(db, path):
    users_file, game_file = path + "/users.csv", path + "/games.csv"
    game_locations_file, users_locations_file, game_letters_file = path + "/game_locations.csv", \
                                                                   path + "/user_locations.csv", \
                                                                   path + "/game_letters.csv",
    score_history_file = path + "/score_history.csv"
    users, games = load_file(users_file), load_file(game_file)
    game_locations, users_locations, game_letters, score_history = load_file(game_locations_file), \
                                                     load_file(users_locations_file), load_file(game_letters_file), \
                                                                   load_file(score_history_file)
    fail_val = -1
    try:
        cursor = db.cursor()
    except mysql.Error as e:
        print("Database connection error")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(5)
    users_table(db, cursor)
    make_users(db, cursor, users)
    create_game_table(db, cursor)
    letter_table(db, cursor)
    locations_table(db, cursor)
    create_games(db, cursor, games, game_locations, users_locations, game_letters, score_history)
    cursor.close()
    return 1





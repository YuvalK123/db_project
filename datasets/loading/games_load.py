import mysql.connector as mysql


def create_game_table(db, cursor):
    # gid, uid, current_score, strikes
    query = "CREATE TABLE games (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
            "uid MEDIUMINT, FOREIGN KEY(uid) REFERENCES users(id), current_score SMALLINT, " \
            "strikes TINYINT, hints TINYINT, current_location SMALLINT UNSIGNED, FOREIGN KEY(current_location) " \
            "REFERENCES locations(id));"
    db.commit()
    cursor.execute(query)
    query = f"CREATE TABLE score_history (uid MEDIUMINT PRIMARY KEY NOT NULL, FOREIGN KEY(uid) REFERENCES users(id), " \
            f"score SMALLINT, datetime DATETIME NOT NULL); "
    cursor.execute(query)
    db.commit()


def letter_table(db, cursor):
    # gid, char
    query = "CREATE TABLE game_letter (gid MEDIUMINT NOT NULL, FOREIGN KEY(gid) REFERENCES games(id), letter CHAR(1)); "
    cursor.execute(query)
    db.commit()


def locations_table(db, cursor):
    # gid, location
    query = "CREATE TABLE game_locations (gid MEDIUMINT NOT NULL, FOREIGN KEY(gid) REFERENCES games(id), " \
            "location SMALLINT UNSIGNED, FOREIGN KEY(location) REFERENCES locations(id)); "
    cursor.execute(query)
    db.commit()
    query = "CREATE TABLE user_locations (uid MEDIUMINT NOT NULL, FOREIGN KEY(uid) REFERENCES users(id), " \
            "location SMALLINT UNSIGNED, FOREIGN KEY(location) REFERENCES locations(id)); "
    cursor.execute(query)
    db.commit()


def users(db, cursor):
    # uid, username, password, age, gender
    query = f"CREATE TABLE users (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(20)," \
            f"password VARCHAR(25), age DATE, gender CHAR(1)); "
    cursor.execute(query)
    db.commit()
    query = f"CREATE TABLE admins (uid MEDIUMINT PRIMARY KEY NOT NULL, FOREIGN KEY(uid) REFERENCES users(id)); "
    cursor.execute(query)
    db.commit()


def make_users(db, cursor):
    username, password, age, gender = "user", 12345, "1994-03-09", "m"
    query = f"INSERT INTO users (username, password, age, gender) " \
            f"VALUES('{username}', {password}, '{age}', '{gender}')"
    cursor.execute(query)
    username, password, age, gender = "user2", 123415, "1992-07-07", "f"
    query = f"INSERT INTO users (username, password, age, gender) " \
            f"VALUES('{username}', {password}, '{age}', '{gender}')"
    cursor.execute(query)
    adminname, password, age, gender = "admin", 123456, "1998-01-31", "f"
    query = f"INSERT INTO users (username, password, age, gender) " \
            f"VALUES('{adminname}', {password}, '{age}', '{gender}')"
    cursor.execute(query)
    db.commit()
    query = f"SELECT id FROM users WHERE username='{adminname}'"
    cursor.execute(query)
    admin_id = cursor.fetchone()
    if admin_id is not None:
        admin_id = admin_id[0]
    print(admin_id)
    query = f"INSERT INTO admins (uid) VALUES({admin_id});"
    cursor.execute(query)
    db.commit()


def create_games(db, cursor):
    # games =  gid, uid, current_score, strikes, current_location, hints
    # locations = gid, location
    # letters = gid, letter
    games = [(1, 1, 122, 2, 4, 2500), (5, 2, 7, 5, 5, 500), (22, 3, 14, 1, 2, 33)]
    game_locations = [(5, 1400), (5, 1412), (22, 502), (1, 202), (1, 305)]
    user_locations = [(1, 202), (1, 305), (2, 1400), (2, 1412), (3, 502)]
    letters = [(1, 'b'), (1, 'f'), (1, 'z'), (5, 'e'), (5, 'm'), (22, 'a'), (22, 'i')]
    query = "INSERT INTO games (id, uid, current_score, strikes, hints, current_location) " \
            "VALUES (%s, %s, %s, %s, %s, %s);"
    cursor.executemany(query, games)
    db.commit()
    print("games")
    query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
    cursor.executemany(query, game_locations)
    db.commit()
    query = "INSERT INTO user_locations (uid, location) VALUES (%s, %s);"
    cursor.executemany(query, user_locations)
    db.commit()
    query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
    cursor.executemany(query, letters)
    db.commit()


def load(db, path):
    cursor = db.cursor()
    users(db, cursor)
    create_game_table(db, cursor)
    letter_table(db, cursor)
    locations_table(db, cursor)
    make_users(db, cursor)
    create_games(db, cursor)

# def main():
#     create_game_table()
#     letter_table()
#     locations_table()
#     users()
#     make_users()
#     create_games()


if __name__ == '__main__':
    main()

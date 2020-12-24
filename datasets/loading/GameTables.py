import mysql.connector as mysql

PASSWORD = "1q2w3E4R"
DATABASE = "GlobalInfoApp"
db = mysql.connect(
    host="localhost",
    user="root",
    passwd=PASSWORD,
    database=DATABASE
)
cursor = db.cursor()


def create_game_table():
    # gid, uid, current_score, strikes
    query = "CREATE TABLE games (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
            "uid MEDIUMINT,current_score SMALLINT, strikes TINYINT, current_location MEDIUMINT);"
    cursor.execute(query)
    query = f"CREATE TABLE score_history (uid MEDIUMINT PRIMARY KEY NOT NULL, score SMALLINT, " \
            f"datetime DATETIME NOT NULL); "
    cursor.execute(query)
    db.commit()


def letter_table():
    # gid, char
    query = "CREATE TABLE game_letter (gid MEDIUMINT NOT NULL, letter CHAR(1)); "
    cursor.execute(query)
    db.commit()


def locations_table():
    # gid, location
    query = "CREATE TABLE game_locations (gid MEDIUMINT NOT NULL, location MEDIUMINT); "
    cursor.execute(query)
    db.commit()


def users():
    # uid, username, password, age, gender
    query = f"CREATE TABLE users (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(20)," \
            f"password VARCHAR(25), age TINYINT, gender CHAR(1)); "
    cursor.execute(query)
    query = f"CREATE TABLE admins (uid MEDIUMINT PRIMARY KEY NOT NULL ); "
    cursor.execute(query)
    db.commit()


def make_users():
    username, password, age, gender = "user", 12345, 26, "m"
    query = f"INSERT INTO users (username, password, age, gender) " \
            f"VALUES('{username}', {password}, {age}, '{gender}')"
    cursor.execute(query)
    adminname, password, age, gender = "admin", 123456, 25, "f"
    query = f"INSERT INTO users (username, password, age, gender) " \
            f"VALUES('{adminname}', {password}, {age}, '{gender}')"
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


def create_games():
    # games =  gid, uid, current_score, strikes, current_location
    # locations = gid, location
    # letters = gid, letter
    games = [(1, 3, 122, 2, 2500), (2, 5, 7, 5, 14000), (3, 22, 14, 1, 33)]
    locations = [(3, 1400), (3, 1412), (3, 502), (1, 202), (2, 305)]
    letters = [(1, 'b'), (1, 'f'), (1, 'z'), (2, 'e'), (2, 'm'), (3, 'a'), (3, 'i')]
    query = "INSERT INTO games (id, uid, current_score, strikes, current_location) " \
            "VALUES (%s, %s, %s, %s, %s);"
    cursor.executemany(query, games)
    query = "INSERT INTO game_locations (gid, location) VALUES (%s, %s);"
    cursor.executemany(query, locations)
    query = "INSERT INTO game_letter (gid, letter) VALUES (%s, %s);"
    cursor.executemany(query, letters)
    db.commit()



def main():
    # create_game_table()
    # letter_table()
    # locations_table()
    users()
    make_users()
    # create_games()


if __name__ == '__main__':
    main()

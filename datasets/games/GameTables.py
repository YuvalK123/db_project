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
            "uid MEDIUMINT,current_score SMALLINT, strikes TINYINT);"
    cursor.execute(query)
    query = f"CREATE TABLE score_history (uid MEDIUMINT PRIMARY KEY NOT NULL, score SMALLINT, " \
            f"datetime DATETIME NOT NULL); "
    cursor.execute(query)
    db.commit()


def letter_table():
    #gid, char
    query = "CREATE TABLE game_letter (gid MEDIUMINT NOT NULL, letter CHAR(1)); "
    cursor.execute(query)
    db.commit()

def locations_table():
    # gid, location
    query = "CREATE TABLE game_locations (gid MEDIUMINT NOT NULL, location MEDIUMINT); "
    cursor.execute(query)
    db.commit()



def users():
    #uid, username, password, age, gender
    query = f"CREATE TABLE users (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(20)," \
            f"password VARCHAR(25), age TINYINT, gender CHAR(1)); "
    cursor.execute(query)
    query = f"CREATE TABLE admins (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(20)," \
            f"password VARCHAR(25), age TINYINT, gender CHAR(1)); "
    cursor.execute(query)
    db.commit()


def make_users():
    username, password, age, gender = "user", 12345, 26, "m"
    query = f"INSERT INTO users (username, password, age, gender) VALUES('{username}', {password}, {age}, '{gender}')"
    print(query)
    cursor.execute(query)
    adminname, password, age, gender = "admin", 123456, 25, "f"
    query = f"INSERT INTO admins (username, password, age, gender) VALUES('{adminname}', {password}, {age}, '{gender}')"
    cursor.execute(query)
    db.commit()

def main():
    # create_game_table()
    # letter_table()
    # locations_table()
    # users()
    make_users()


if __name__ == '__main__':
    main()
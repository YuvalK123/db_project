import mysql.connector as mysql
import os
from fast_people_load import load as people_load
from games_load import load as game_load
from restaurants_load import load as res_loas
from cinema_load import load as cinema_load
PASSWORD = "1q2w3E4R"
DATABASE = "GlobalInfoApp"

def create_database(db):
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE GlobalInfoApp")
    db.commit()


def main():
    try:
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd=PASSWORD,
            database=DATABASE
        )
    except mysql.Error as err:
        print(err)
        exit(2)
    except Exception as e:
        print(e)
        exit(3)
    cinema_dir = os.path.realpath('../cinema').replace("\\", "/")
    restaurants_dir = os.path.realpath('../Restaurants').replace("\\", "/")
    people_dir = os.path.realpath('../people').replace("\\", "/")
    games_dir = os.path.realpath('../general').replace("\\", "/")

    print("loading locations and people tables...")
    status = people_load(db, people_dir)
    if status < 0:
        return status
    print("done loading locations/people")
    print("loading restaurants table...")
    status = res_loas(db, restaurants_dir)
    if status < 0:
        return status
    print("done restaurants")
    print("loading cinema tables...")
    status = cinema_load(db, cinema_dir)
    if status < 0:
        return status
    print("done loading cinema")
    print("loading games/users tables...")
    status = game_load(db, games_dir)
    if status < 0:
        return status
    print("done games/users tables")
    print("Done loading!")
    # curr_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


if __name__ == '__main__':
    main()
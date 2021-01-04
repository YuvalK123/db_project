import mysql.connector as mysql
import os, csv
from fast_people_load import load as people_load
from games_load import load as game_load
from restaurants_load import load as res_loas
from cinema_load import load as cinema_load
PASSWORD = "topaz083@gmail.comTT"
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
        # create_database(db)
        cinema_dir = os.path.realpath('../cinema').replace("\\", "/")
        restaurants_dir = os.path.realpath('../Restaurants').replace("\\", "/")
        people_dir = os.path.realpath('../people').replace("\\", "/")
    except Exception as e:
        print(e)
        exit(55)
    people_load(db, people_dir)
    res_loas(db, restaurants_dir)
    cinema_load(db, cinema_dir)
    game_load(db, "")

    curr_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


if __name__ == '__main__':
    main()
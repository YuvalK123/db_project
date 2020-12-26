import mysql.connector as mysql
import sys
import pickle


PASSWORD = "1q2w3E4R"
DATABASE = "GlobalInfoApp"


# def main():
    # enter here your personal info for MySql
    # db = mysql.connect(
    #     host="127.0.0.1",
    #     user="root",
    #     passwd=PASSWORD,
    #
    # )
    #
    # cursor = db.cursor()
    # cursor.execute("CREATE DATABASE GlobalInfoApp")

    # after creating a data base, comment the commands above and uncomment the upcoming commands.
    #
    # db = mysql.connect(
    #     host="127.0.0.1",
    #     user="root",
    #     passwd=PASSWORD,
    #     database=DATABASE
    # )
    #
    # cursor = db.cursor()
    # # create table of countries. it is important that the file of the data will be places in the location specified.
    # cursor.execute("CREATE TABLE res_temp (id VARCHAR(45), "
    #                "name VARCHAR(100), city_id VARCHAR(45) NULL, address VARCHAR(400), latitude VARCHAR(45) NULL, "
    #                "longitude VARCHAR(45), cousine VARCHAR(1450), url VARCHAR(1450));")
    # cursor.execute("SET GLOBAL local_infile=1;")
    # path = "D:/Db/restaurants"
    # query = f"LOAD DATA INFILE '{path}/Datafiniti_Fast_Food_Restaurants_May19US.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE '{path}/one-star-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE '{path}/starbucks locations.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE '{path}/three-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE '{path}/two-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    #
    # cursor.execute("CREATE TABLE restaurants (id VARCHAR(45), "
    #                "name VARCHAR(100), city_id VARCHAR(45) NULL, address VARCHAR(400), latitude VARCHAR(45) NULL, "
    #                "longitude VARCHAR(45), cousine VARCHAR(1450), url VARCHAR(1450));")
    # query = "INSERT INTO restaurants (id, name, city_id, address, latitude, longitude, cousine, url) SELECT id, name, city_id, address, latitude, longitude, cousine, url " \
    #         "FROM res_temp;"
    # cursor.execute(query)
    # # cursor.execute('DROP TABLE countries_temp')
    # db.commit()
    #
    # with open("backup.txt", "rb") as fp:  # Unpickling
    #     all_info = pickle.load(fp)


def load(db, path):
    # cursor = db.cursor()
    # cursor.execute("CREATE DATABASE GlobalInfoApp")

    # after creating a data base, comment the commands above and uncomment the upcoming commands.


    cursor = db.cursor()
    # create table of countries. it is important that the file of the data will be places in the location specified.
    cursor.execute("CREATE TABLE res_temp (id VARCHAR(45), "
                   "name VARCHAR(100), city_id VARCHAR(45) NULL, address VARCHAR(400), latitude VARCHAR(45) NULL, "
                   "longitude VARCHAR(45), cousine VARCHAR(1450), url VARCHAR(1450));")

    query = f"LOAD DATA INFILE '{path}/Datafiniti_Fast_Food_Restaurants_May19US.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/one-star-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/starbucks locations.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/three-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/two-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)

    cursor.execute("CREATE TABLE restaurants (id VARCHAR(45), "
                   "name VARCHAR(100), city_id VARCHAR(45) NULL, address VARCHAR(400), latitude VARCHAR(45) NULL, "
                   "longitude VARCHAR(45), cousine VARCHAR(1450), url VARCHAR(1450));")
    query = "INSERT INTO restaurants (id, name, city_id, address, latitude, longitude, cousine, url) SELECT id, name, city_id, address, latitude, longitude, cousine, url " \
            "FROM res_temp;"
    cursor.execute(query)
    # cursor.execute('DROP TABLE countries_temp')
    db.commit()





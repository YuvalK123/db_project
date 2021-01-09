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
    cursor.execute("CREATE TABLE `rest_temp` (`name` VARCHAR(256) NULL,`city_id` VARCHAR(45) NULL,`latitude` FLOAT NULL,`longitude` FLOAT NULL,`url` VARCHAR(1000) NULL)")


    query = f"LOAD DATA INFILE '{path}/Datafiniti_Fast_Food_Restaurants_May19US.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/one-star-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/starbucks locations.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/three-stars-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    query = f"LOAD DATA INFILE '{path}/two-stars-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    cursor.execute(query)
    db.commit()

    cursor = db.cursor()
    query = f"CREATE TABLE `restaurants` (`name` VARCHAR(256) NULL,`city_id` SMALLINT UNSIGNED NULL,`latitude` FLOAT NULL,`longitude` FLOAT NULL,  `url` VARCHAR(1000) NULL,   INDEX `fk1_idx` (`city_id` ASC) VISIBLE,  CONSTRAINT `fk1`    FOREIGN KEY (`city_id`)    REFERENCES `locations` (`id`) );"
    try:
        cursor.execute(query)
        db.commit()
    except Exception as e:  # table created
        print("e", e)
        pass
    # gets pid and movieId
    id_name_query = " SELECT id, Location FROM locations"
    cursor.execute(id_name_query)
    locations = cursor.fetchall()
    loc_dict = {}
    for x in locations:
        if x[0] and x[1]:
            loc_dict[x[1]] = x[0]
    query = " SELECT * FROM rest_temp"
    cursor.execute(query)
    rests = cursor.fetchall()

    for rest in range(len(rests)):
        rests[rest] = list(rests[rest])
        if (rests[rest][1] in loc_dict):
            rests[rest][1] = loc_dict[rests[rest][1]]
        else:
            rests[rest][1] = "-1"
    final_rests = []
    for rest in range(len(rests)):
        if rests[rest][1] != "-1" and rests[rest][1] is not None:
            final_rests.append(rests[rest])

    query = f"INSERT INTO restaurants (name,city_id,latitude,longitude,url) VALUES (%s, %s,%s, %s, %s);"
    cursor.executemany(query, final_rests)
    db.commit()

    query = "ALTER TABLE `restaurants` ADD COLUMN `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT FIRST,ADD PRIMARY KEY (`id`);"
    cursor.execute(query)
    db.commit()

    cursor.execute("DROP TABLE rest_temp")
    db.commit()


import mysql.connector as mysql


PASSWORD = "1q2w3E4R"
DATABASE = "GlobalInfoApp"

def load(db, path):
    # cursor = db.cursor()
    # cursor.execute("CREATE DATABASE GlobalInfoApp")

    # after creating a data base, comment the commands above and uncomment the upcoming commands.
    fail_val = -1
    try:
        cursor = db.cursor()
    except mysql.Error as e:
        print("Database connection error")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(4)
    try:
        # create table of countries. it is important that the file of the data will be places in the location specified.
        cursor.execute("CREATE TABLE `rest_temp` (`name` VARCHAR(256) NULL,`city_id` VARCHAR(45) NULL, "
                       "`latitude` FLOAT NULL,`longitude` FLOAT NULL,`url` VARCHAR(1000) NULL)")
    except mysql.Error as e:
        print("rest_temp creation table fail")
        print(e)
    except Exception as e:
        print(e)
        exit(5)
    try:
        query = f"LOAD DATA INFILE '{path}/Datafiniti_Fast_Food_Restaurants_May19US.csv' " \
                f"INTO TABLE rest_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' " \
                f"IGNORE 1 LINES;"
        cursor.execute(query)
        query = f"LOAD DATA INFILE '{path}/one-star-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS " \
                f"TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
        cursor.execute(query)
        query = f"LOAD DATA INFILE '{path}/starbucks locations.csv' INTO TABLE rest_temp FIELDS TERMINATED BY ',' " \
                f"ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
        cursor.execute(query)
        query = f"LOAD DATA INFILE '{path}/three-stars-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS " \
                f"TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
        cursor.execute(query)
        query = f"LOAD DATA INFILE '{path}/two-stars-michelin-restaurants.csv' INTO TABLE rest_temp FIELDS " \
                f"TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("rest_temp table loading fail")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(6)


    query = f"CREATE TABLE `restaurants` (`name` VARCHAR(256) NULL,`city_id` SMALLINT UNSIGNED NULL," \
            f"`latitude` FLOAT NULL,`longitude` FLOAT NULL,  `url` VARCHAR(1000) NULL, " \
            f"INDEX `fk1_idx` (`city_id` ASC) VISIBLE,  CONSTRAINT `fk1` FOREIGN KEY (`city_id`) " \
            f"REFERENCES `locations` (`id`) );"
    try:
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("restaurants table creation fail")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(7)
    # gets pid and movieId
    try:
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
    except mysql.Error as e:
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(8)

    for rest in range(len(rests)):
        rests[rest] = list(rests[rest])
        if (rests[rest][1] in loc_dict):
            rests[rest][1] = loc_dict[rests[rest][1]]
        else:
            rests[rest][1] = "-1"
        if "," in rests[rest][4]:
            rests[rest][4] = rests[rest][4].split(",")[0]
    final_rests = []
    for rest in range(len(rests)):
        if rests[rest][1] != "-1" and rests[rest][1] is not None:
            final_rests.append(rests[rest])
    try:
        query = f"INSERT INTO restaurants (name,city_id,latitude,longitude,url) VALUES (%s, %s,%s, %s, %s);"
        cursor.executemany(query, final_rests)
        db.commit()

        query = "ALTER TABLE `restaurants` ADD COLUMN `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT FIRST," \
                "ADD PRIMARY KEY (`id`);"
        cursor.execute(query)
        db.commit()

        cursor.execute("DROP TABLE rest_temp")
        db.commit()
    except mysql.Error as e:
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(8)
    return 1


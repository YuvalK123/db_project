import mysql.connector as mysql

def load(db, path):
    fail_val = -1
    try:
        cursor = db.cursor()
        cursor.execute("SET GLOBAL local_infile=1;")
    except mysql.Error as e:
        print("Database connection error")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(4)
    # locations table
    try:
        cursor.execute("CREATE TABLE locations (id SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, "
                       "Location VARCHAR(70));")
        query = f"LOAD DATA INFILE '{path}/locations.csv' INTO TABLE locations " \
                "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("locations table fail")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(5)

    # job_type table
    try:
        cursor.execute("CREATE TABLE job_type (id BIT(1) PRIMARY KEY NOT NULL, Job VARCHAR(10));")
        query = f"LOAD DATA INFILE '{path}/job_type.csv' INTO TABLE job_type " \
                "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("job type table fail")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(6)

    # people_info table
    try:
        cursor.execute("CREATE TABLE people_info (id MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, "
                   "Name VARCHAR(70), Gender CHAR(1), BornIn SMALLINT UNSIGNED,"
                   "FOREIGN KEY(BornIn) REFERENCES locations(id), DiedIn SMALLINT UNSIGNED, "
                   "FOREIGN KEY(DiedIn) REFERENCES locations(id));")
        query = f"LOAD DATA INFILE '{path}/people_info.csv' INTO TABLE " \
                "people_info FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
        cursor.execute(query)
        db.commit()
    except mysql.Error as e:
        print("job type table fail")
        print(e)
        return fail_val
    except Exception as e:
        print(e)
        exit(7)
    cursor.close()
    return 1


import mysql.connector as mysql
import pickle
import datetime
from dateutil.relativedelta import relativedelta

def main():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="topaz083@gmail.comTT",
        database="GlobalInfoApp"
    )

    cursor = db.cursor()

    # create a cities table (it will help us but won't remain)
    # create table of countries. it is important that the file of the data will be places in the location specified.
    # cursor.execute("CREATE TABLE countries (Country CHAR(2), "
    #                "City VARCHAR(100), AccentCity VARCHAR(100) NULL, Region VARCHAR(4), Population INT NULL, "
    #                "Latitude FLOAT(9,6), Longitude FLOAT(9,6));")
    # cursor.execute("SET GLOBAL local_infile=1;")
    # query = "LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/countries.csv' INTO TABLE countries " \
    #         "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (Country, City, " \
    #         "AccentCity, Region, @vPopulation, Latitude, Longitude) SET Population = NULLIF(" \
    #         "@vPopulation,''); "
    # cursor.execute(query)
    # cursor.execute("CREATE TABLE cities (Id int PRIMARY KEY NOT NULL AUTO_INCREMENT, City VARCHAR(100));")
    # query = "INSERT INTO cities (City) SELECT City FROM countries;"
    # cursor.execute(query)
    # cursor.execute('DROP TABLE countries')
    # db.commit()

    # create the job type table.
    # cursor.execute("CREATE TABLE job_type (id BIT(1) PRIMARY KEY NOT NULL, Job VARCHAR(10));")
    # cursor.execute("INSERT INTO job_type VALUES(0, 'Actor');")
    # cursor.execute("INSERT INTO job_type VALUES(1, 'Director');")
    # db.commit()
    # cursor.execute('DROP TABLE people_info_temp')
    # # create the people info table.
    # cursor.execute("CREATE TABLE people_info_temp (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
    #                "Gender VARCHAR(7), BornIn VARCHAR(70), DiedIn VARCHAR(70), Job_id BIT(1), FOREIGN KEY(Job_id) "
    #                "REFERENCES job_type(id));")
    #
    # # creates temp people info table
    # with open("backup_updated.txt", "rb") as fp:  # Unpickling
    #     all_info = pickle.load(fp)
    #
    # query_people = "INSERT INTO people_info_temp (Name, Gender, BornIn, DiedIn, Job_id) VALUES (%s, %s, %s, %s, %s)"
    # counter = 0
    # for item in all_info:
    #     if len(item) == 2 or (len(item) == 6 and not (item[5] == '' or item[4] == item[5])) or len(item) >= 7:
    #         continue
    #     if len(item) == 3:
    #         item.append('')
    #     if len(item) == 4:
    #         item.append('')
    #
    #     values = (item[0].strip(), item[4].strip(), item[2].strip(), item[3].strip(), item[1])
    #     print(counter, item[4], len(item[4]), item)
    #     cursor.execute(query_people, values)
    # db.commit()
    # #
    # # # fix locations so the location will contain only a city
    # cursor.execute("SELECT City FROM cities")
    # cities = [x[0] for x in cursor.fetchall()]
    # cursor.execute("SELECT BornIn, DiedIn FROM people_info_temp")
    # temp_info = cursor.fetchall()
    # temp_born = [x[0] for x in temp_info]
    # temp_died = [x[1] for x in temp_info]
    #
    # sql_born = "UPDATE people_info_temp SET BornIn = %s WHERE BornIn = %s"
    # for loc in temp_born:
    #     born_in = loc
    #     if born_in.find(',') > 0:
    #         sep_string = born_in.split(',')
    #         for x in sep_string:
    #             x = x.lower().replace('city', '').strip()
    #             if x in cities:
    #                 born_in = x
    #                 break
    #         if born_in.find(',') > 0:
    #             born_in = None
    #     elif not born_in.isascii() or (born_in.lower().replace('city', '').strip() not in cities and born_in != ''):
    #         born_in = None
    #
    #     if born_in == '' or born_in == ' ':
    #         born_in = None
    #
    #     if (loc != born_in and loc != '') or born_in is None:
    #         val = (born_in, loc)
    #         cursor.execute(sql_born, val)
    #
    # sql_died = "UPDATE people_info_temp SET DiedIn = %s WHERE DiedIn = %s"
    # for loc in temp_died:
    #     died_in = loc
    #     if died_in.find(',') > 0:
    #         sep_string = died_in.split(',')
    #         for x in sep_string:
    #             x = x.lower().replace('city', '').strip()
    #             if x in cities:
    #                 died_in = x
    #                 break
    #         if died_in.find(',') > 0:
    #             died_in = None
    #     elif not died_in.isascii() or (died_in.lower().replace('city', '').strip() not in cities and died_in != ''):
    #         died_in = None
    #
    #     if died_in == '' or died_in == ' ':
    #         died_in = None
    #
    #     if (loc != died_in and loc != '') or died_in is None:
    #         val = (died_in, loc)
    #         cursor.execute(sql_died, val)
    #
    # db.commit()

    # create res_temp
    # cursor.execute("DROP TABLE res_temp")
    # cursor.execute("CREATE TABLE res_temp (id VARCHAR(50), name VARCHAR(256) NULL,city_id VARCHAR(45), "
    #                "address VARCHAR(270) NULL,latitude VARCHAR(45) NULL, longitude VARCHAR(45) NULL, cuisine VARCHAR("
    #                "1000) NULL, url VARCHAR(1000) NULL);")
    #
    #
    # query = f"LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Datafiniti_Fast_Food_Restaurants_May19US.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/one-star-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/starbucks locations.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/three-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # query = f"LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/two-stars-michelin-restaurants.csv' INTO TABLE res_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # db.commit()
    #
    # # creates locations table
    # cursor.execute('DROP TABLE people_info')
    # cursor.execute('DROP TABLE locations')
    # cursor.execute("CREATE TABLE locations_temp (Location VARCHAR(70));")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT BornIn FROM people_info_temp;")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT DiedIn FROM people_info_temp;")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT city_id FROM res_temp;")
    # cursor.execute("CREATE TABLE locations (id SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, Location VARCHAR("
    #                "70));")
    # cursor.execute("INSERT INTO locations (Location) SELECT DISTINCT Location FROM locations_temp;")
    # cursor.execute('DROP TABLE locations_temp')
    # # remove white spaces in location column in locations table
    # cursor.execute("UPDATE locations SET location = TRIM(location);")
    # # deletes the NULL row
    # cursor.execute("DELETE FROM locations WHERE Location IS NULL;")
    # db.commit()
    # # create people_info final table
    # cursor.execute("CREATE TABLE people_info (id MEDIUMINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, "
    #                "Name VARCHAR(70), Gender CHAR(1), BornIn SMALLINT UNSIGNED ,FOREIGN KEY(BornIn) REFERENCES "
    #                "locations(id), DiedIn SMALLINT UNSIGNED, "
    #                "FOREIGN KEY(DiedIn) REFERENCES locations(id));")
    #
    # cursor.execute("SELECT * FROM locations;")
    # loc_result = cursor.fetchall()
    # id_list = [x[0] for x in loc_result if x[1] is not None]
    # loc_list = [x[1].lower() for x in loc_result if x[1] is not None]
    # cursor.execute("SELECT * FROM people_info_temp;")
    # people_result = cursor.fetchall()
    # query_people = "INSERT INTO people_info (Name, Gender, BornIn, DiedIn) VALUES (%s, %s, %s, %s)"
    # for row in people_result:
    #     born_in = row[3]
    #     died_in = row[4]
    #     if row[3] is not None:
    #         born_in = row[3].strip().lower()
    #         if born_in == 'høyland':
    #             born_in = 'hoyland '
    #     if row[4] is not None:
    #         died_in = row[4].strip().lower()
    #     gender = row[2].strip().lower()
    #     if gender == 'male':
    #         gender = 'm'
    #     else:
    #         gender = 'f'
    #
    #     if not (born_in is None and died_in is None):
    #         if born_in is None:
    #             values = (row[1].strip(), gender, None, id_list[loc_list.index(died_in)])
    #         elif died_in is None:
    #             values = (row[1].strip(), gender, id_list[loc_list.index(born_in)], None)
    #         else:
    #             values = (
    #                 row[1].strip(), gender, id_list[loc_list.index(born_in)], id_list[loc_list.index(died_in)])
    #         cursor.execute(query_people, values)
    # db.commit()

    # creating csv files from the tables created to fast load
    # cursor.execute("SELECT *  FROM locations INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server "
    #                "8.0/Uploads/locations.csv' FIELDS ENCLOSED BY '\"' TERMINATED BY ',' LINES "
    #                "TERMINATED BY '\r\n';")
    # cursor.execute("SELECT *  FROM people_info INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server "
    #                "8.0/Uploads/people_info.csv' FIELDS ENCLOSED BY '\"' TERMINATED BY ',' LINES "
    #                "TERMINATED BY '\r\n';")
    # cursor.execute("SELECT * FROM job_type INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server "
    #                "8.0/Uploads/job_type.csv' FIELDS ENCLOSED BY '\"' TERMINATED BY ',' LINES "
    #                "TERMINATED BY '\r\n';")

    # cursor.execute('DROP TABLE people_info_temp')
    # cursor.execute('DROP TABLE cities')


if __name__ == '__main__':
    main()

import mysql.connector as mysql
import sys
import pickle


def main():
    # enter here your personal info for MySql
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="password",
    )

    cursor = db.cursor()
    cursor.execute("CREATE DATABASE GlobalInfoApp")

    # after creating a data base, comment the commands above and uncomment the upcoming commands.

    # db = mysql.connect(
    #    host="localhost",
    #    user="root",
    #    passwd="password",
    #    database="GlobalInfoApp"
    # )

    # cursor = db.cursor()
    # create table of countries. it is important that the file of the data will be places in the location specified.
    # cursor.execute("CREATE TABLE countries_temp (Country CHAR(2), "
    #               "City VARCHAR(100), AccentCity VARCHAR(100) NULL, Region VARCHAR(4), Population VARCHAR(10) NULL, "
    #               "Latitude FLOAT(9,6), Longitude FLOAT(9,6));")
    # cursor.execute("SET GLOBAL local_infile=1;")
    # query = "LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/countries.csv' INTO TABLE countries_temp FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    # cursor.execute(query)
    # cursor.execute("CREATE TABLE countries (Id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Country CHAR(2), "
    #               "City VARCHAR(100), Latitude FLOAT(9,6), Longitude FLOAT(9,6));")
    # query = "INSERT INTO countries (Country, City, Latitude, Longitude) SELECT Country, City, Latitude, Longitude " \
    #        "FROM countries_temp;"
    # cursor.execute(query)
    # cursor.execute('DROP TABLE countries_temp')
    # db.commit()

    # create the people info table.
    # cursor.execute("CREATE TABLE people_info (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
    #               "Gender VARCHAR(7), BornIn VARCHAR(70), DiedIn VARCHAR(70));")

    # with open("backup.txt", "rb") as fp:  # Unpickling
    #    all_info = pickle.load(fp)

    # query_people = "INSERT INTO people_info (Name, Gender, BornIn, DiedIn) VALUES (%s, %s, %s, %s)"
    # counter = 0
    # for item in all_info:
    #    if len(item) == 1 or len(item) > 4:
    #        continue
    #    if len(item) == 2:
    #        item.append('')
    #    if len(item) == 3:
    #        item.append('')
    #    values = (item[0], item[3], item[1], item[2])
    #    print(counter, item[3], len(item[3]), item)
    #    cursor.execute(query_people, values)
    # db.commit()


if __name__ == '__main__':
    main()

import mysql.connector as mysql
import pickle


def main():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="topaz083@gmail.comTT",
        database="GlobalInfoApp"
    )

    cursor = db.cursor()

    # create the job type table.
    # cursor.execute("CREATE TABLE job_type (id BIT(1) PRIMARY KEY NOT NULL, Job VARCHAR(10));")
    # cursor.execute("INSERT INTO job_type VALUES(0, 'Actor');")
    # cursor.execute("INSERT INTO job_type VALUES(1, 'Director');")
    # db.commit()

    # create the people info table.
    # cursor.execute('DROP TABLE people_info')
    # cursor.execute("CREATE TABLE people_info (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
    #               "Gender VARCHAR(7), BornIn VARCHAR(70), DiedIn VARCHAR(70), Job_id BIT(1), FOREIGN KEY(Job_id) "
    #               "REFERENCES job_type(id));")

    # creates temp people info table
    # with open("backup_bad.txt", "rb") as fp:  # Unpickling
    #     all_info = pickle.load(fp)
    #
    # cursor.execute('DROP TABLE people_info')
    # cursor.execute("CREATE TABLE people_info (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
    #                "Gender VARCHAR(7), BornIn VARCHAR(70), DiedIn VARCHAR(70), Job_id BIT(1), FOREIGN KEY(Job_id) "
    #                "REFERENCES job_type(id));")
    # query_people = "INSERT INTO people_info (Name, Gender, BornIn, DiedIn, Job_id) VALUES (%s, %s, %s, %s, %s)"
    # counter = 0
    # for item in all_info:
    #     if len(item) == 2 or (len(item) == 6 and not (item[5] == '' or item[4] == item[5])) or len(item) >= 7:
    #         continue
    #     if len(item) == 3:
    #         item.append('')
    #     if len(item) == 4:
    #         item.append('')
    #
    #     values = (item[0], item[4], item[2], item[3], item[1])
    #     print(counter, item[4], len(item[4]), item)
    #     cursor.execute(query_people, values)
    # db.commit()

    # creates locations table
    # cursor.execute('DROP TABLE locations')
    # cursor.execute("CREATE TABLE locations_temp (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Location VARCHAR(70));")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT BornIn FROM people_info;")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT DiedIn FROM people_info;")
    # cursor.execute("INSERT INTO locations_temp (Location) SELECT city_id FROM res_temp;")
    # cursor.execute("CREATE TABLE locations (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Location VARCHAR(70));")
    # cursor.execute("INSERT INTO locations (Location) SELECT DISTINCT location FROM locations_temp;")
    # cursor.execute('DROP TABLE locations_temp')
    # db.commit()

    # cursor.execute("CREATE TABLE people_info_table (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
    #                "Gender VARCHAR(7), BornIn int ,FOREIGN KEY(BornIn) REFERENCES locations(id), DiedIn int ,"
    #                "FOREIGN KEY(DiedIn) REFERENCES locations(id), Job_id BIT(1), FOREIGN KEY(Job_id) REFERENCES "
    #                "job_type(id));")

    # cursor.execute("SELECT * FROM locations;")
    # loc_result = cursor.fetchall()
    # id_list = [x[0] for x in loc_result]
    # loc_list = [x[1] for x in loc_result]
    #
    # cursor.execute("SELECT * FROM people_info;")
    # people_result = cursor.fetchall()
    #
    # query_people = "INSERT INTO people_info (Name, Gender, BornIn, DiedIn, Job_id) VALUES (%s, %s, %s, %s, %s)"
    # for row in people_result:
    #     print(row[3], row[4])
    #     born_in = row[3]
    #     died_in = row[4]
    #     if born_in.strip() == 'Høyland':
    #         born_in = 'Hoyland '
    #     values = (row[1].strip(), row[2].strip(), id_list[loc_list.index(born_in)], id_list[loc_list.index(died_in)],
    #               row[5])
    #     cursor.execute(query_people, values)
    # cursor.execute('DROP TABLE people_info')
    # db.commit()

    # remove white spaces in location column in locations table
    # cursor.execute("UPDATE locations SET location = TRIM(location);")
    # db.commit()


if __name__ == '__main__':
    main()

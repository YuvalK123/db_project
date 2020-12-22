import mysql.connector as mysql
import pickle


def main():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="topaz083@gmail.comTT",
        database="GlobalInfoApp"
    )

    # cursor = db.cursor()

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
    # cursor.execute("CREATE TABLE locations (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Location VARCHAR(70));")
    # cursor.execute(
    #     "INSERT INTO locations (Location) (SELECT BornIn FROM people_info) UNION (SELECT DiedIn FROM people_info) "
    #     "UNION (SELECT city_id FROM res_temp); ")
    # db.commit()


if __name__ == '__main__':
    main()

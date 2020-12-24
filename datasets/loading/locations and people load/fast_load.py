import mysql.connector as mysql


def main():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="topaz083@gmail.comTT",
        database="GlobalInfoApp"
    )

    cursor = db.cursor()
    cursor.execute("SET GLOBAL local_infile=1;")
    # locations table
    cursor.execute("CREATE TABLE locations (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Location VARCHAR(70));")
    query = "LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/locations.csv' INTO TABLE locations " \
            "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
    cursor.execute(query)
    # job_type table
    cursor.execute("CREATE TABLE job_type (id BIT(1) PRIMARY KEY NOT NULL, Job VARCHAR(10));")
    query = "LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/job_type.csv' INTO TABLE job_type " \
            "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
    cursor.execute(query)
    # people_info table
    cursor.execute("CREATE TABLE people_info (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, Name VARCHAR(70), "
                   "Gender CHAR(1), BornIn int ,FOREIGN KEY(BornIn) REFERENCES locations(id), DiedIn int ,"
                   "FOREIGN KEY(DiedIn) REFERENCES locations(id), Job_id BIT(1), FOREIGN KEY(Job_id) REFERENCES "
                   "job_type(id));")
    query = "LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/people_info.csv' INTO TABLE " \
            "people_info FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'; "
    cursor.execute(query)
    db.commit()


if __name__ == '__main__':
    main()

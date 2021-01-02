import mysql.connector as mysql
import csv

PASSWORD = "1q2w3E4R"
DATABASE = "GlobalInfoApp"

########## Helper Functions  ############
def convert_list_to_string(row, delimiter=', '):
    """
    :param row: array to convert row to string
    :param delimiter: between values
    :return: final row
    """
    row.sort()
    str_row, final_row = [str(w) for w in set(row)], ""
    if len(row) == 1:
        final_row = str_row[0]
    elif len(row) > 1:
        final_row = delimiter.join(str_row)
    return final_row


def convert_list_to_dict(array, replace=False):
    """
    :param array: to convert to dictionary
    :param replace: True to replace keys with values
    :return: dictionary from array
    """
    dic = dict(array)
    if not replace:
        return dic
    new_dic = {}
    for key, val in dic.items():
        new_dic[val] = key
    return new_dic


def generate_rand_genres(genres_keys):
    import random
    num, genres = random.randint(1, 4), []
    genres_keys = [g for g in genres_keys]
    for i in range(num):
        genres.append(random.choice(genres_keys))
    return genres


def get_mapping_table(db, query=" SELECT id, genre FROM genres "):
    """

    :return: dictionary mapping genres to their ids
    """
    cursor, final_genres = db.cursor(), []
    cursor.execute(query)
    genres = cursor.fetchall()  # [(1, 'western'), ...]
    return convert_list_to_dict(genres, True)


def csv_to_dict(file_name):
    dic = {}
    with open(file_name, 'r', encoding="utf-16") as csv_file:
        reader = csv.reader(csv_file)
        # row = next(reader)
        # print(row)
        for row in reader:
            # print(row)
            if len(row) == 0:
                continue
            dic[row[0]] = row[1].strip("][").split(', ')
    # print(dic)
    return dic
#######################################################


def pid_table(db, movies, id_val, table_title="people_movies"):
    """
    function creates table with the given title for (pid, movieId)
    :param db: database connection
    :param movies: dictionary {person: [movies],...}
    :param id_val: 0 if actor, 1 if director
    :param table_title: title of table
    :return: None
    """
    cursor = db.cursor()
    # query = f"CREATE TABLE {table_title} (pid MEDIUMINT, FOREIGN KEY(pid) REFERENCES people_info(id), " \
    #         f"movieId MEDIUMINT, FOREIGN KEY(movieId) REFERENCES movies(id));"
    query = f"CREATE TABLE {table_title} (pid MEDIUMINT UNSIGNED, FOREIGN KEY(pid) REFERENCES people_info(id)," \
            f"movieId MEDIUMINT, FOREIGN KEY(movieId) REFERENCES movies(id), Job_id BIT(1), " \
            f"FOREIGN KEY(Job_id) REFERENCES job_type(id));"
    try:
        cursor.execute(query)
        db.commit()
    except Exception as e:  # table created
        print("e", e)
        pass
    # gets pid and movieId
    id_name_query = " SELECT id, movieName FROM movies "
    cursor.execute(id_name_query)
    movies_rows = cursor.fetchall()  # [(17521, 'Out of Bounds'), (17522, 'Slave Girls from Beyond Infinity'), ...]
    movies_rows = convert_list_to_dict(movies_rows, replace=True)
    id_name_query = " SELECT id, name FROM people_info "
    cursor.execute(id_name_query)
    people = cursor.fetchall()  # [(62887, 'Levan_Abashidze'), (62888, 'LaVan_Davis'), ...]
    people = convert_list_to_dict(people, True)
    # format people name
    new_people = {}
    for person, val in people.items():
        new_person = person.replace('_', ' ')
        x = new_person.find("(")
        if x > 0:
            new_person = new_person[:x - 2]
        new_people[new_person] = val
    people_keys = new_people.keys()
    # converts movies to [(pid, movieId)]
    list_commit = []
    for person, movies in movies.items():
        if person not in people_keys:
            continue
        person_id = new_people[person]
        for movie in movies:
            m = movie.strip("'")
            if m not in movies_rows.keys():
                continue
            movie_id = movies_rows[m]
            list_commit.append((person_id, movie_id, id_val))
    # insert values
    n = len(list_commit) // 5
    batches = [list_commit[i * n:(i + 1) * n] for i in range((len(list_commit) + n - 1) // n)]
    for batch in batches:
        query = f"INSERT INTO {table_title} (pid, movieId, Job_id) VALUES (%s, %s, %s);"
        cursor.executemany(query, batch)
        db.commit()


def genres_table(db, genres):
    """
    functions generates genres table
    :param db: database connection
    :param genres: set of genres
    :return: None
    """
    genres_db = [(genre.strip("'"),) for genre in genres]
    max_len = len(max(genres, key=len)) + 10  # , key=lambda t: len(t)) + 10
    cursor = db.cursor()
    query = f"CREATE TABLE genres (id TINYINT PRIMARY KEY NOT NULL AUTO_INCREMENT, genre VARCHAR({max_len}));"
    cursor.execute(query)
    db.commit()

    query = "INSERT INTO genres (genre) VALUES (%s)"
    cursor.executemany(query, genres_db)
    db.commit()


def get_genres(movies_genres):
    genres = set()
    for genre in movies_genres.values():
        for g in genre:
            genres.add(str(g))
            # print("g", g, genres)
    return genres


def movies_genres_table(db, movies_genres, table_title="movies_genres"):
    """
    :param db: database connection
    :param table_title: title of table
    :param movies_genres: dictionary {movie: [genres], ...}
    :return: None
    """
    final_list = []
    cursor = db.cursor()
    genres_map = get_mapping_table(db, "SELECT id, genre FROM genres")
    movies_maps = get_mapping_table(db, "SELECT id, movieName FROM movies")
    query = f"CREATE TABLE {table_title} (movieId MEDIUMINT, FOREIGN KEY(movieId) REFERENCES movies(id)," \
            f"genreId TINYINT, FOREIGN KEY(genreId) REFERENCES genres(id));"
    try:
        cursor.execute(query)
        db.commit()
    except Exception as e:  # table was created or database connection
        print(e)
        pass
    for movie, genres in movies_genres.items():
        genres_ids = genres_to_id(genres, genres_map)
        for g in genres_ids:
            final_list.append((movies_maps[movie], g))
    n = len(final_list) // 5
    batches = [final_list[i * n:(i + 1) * n] for i in range((len(final_list) + n - 1) // n)]
    query = f"INSERT INTO {table_title} (movieId, genreId) VALUES (%s, %s);"
    for batch in batches:
        cursor.executemany(query, batch)
        db.commit()


def genres_to_id(genres_to_conv, genres_map):
    final_genres = []
    for genre in genres_to_conv:
        final_genres.append(genres_map[genre.strip("'")])
    return final_genres


def movies_table(db, movies_genres):
    """
    functions creates movies table
    :param db: database connection
    :param movies_genres: [(movie, [genres]), ...]
    :return: None
    """
    cursor, keys = db.cursor(), movies_genres.keys()
    values = [(name,) for name in keys]
    max_movie_len = len(max(values, key=lambda t: len(t[0]))[0]) + 10
    query = f"CREATE TABLE movies (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
            f"movieName VARCHAR({max_movie_len}));"
    print(max_movie_len, query)
    try:
        cursor.execute(query)
        db.commit()
    except Exception as e:  # table exists
        pass
    query = "INSERT INTO movies (movieName) VALUES (%s);"

    cursor.executemany(query, values)
    db.commit()

def load(db, path):
    actors_movies_path, directors_movies_path = f"{path}/actors_movies.csv", f"{path}/directors_movies.csv"
    movies_genres_path = f"{path}/people_genres.csv"
    directors_movies, actors_movies = csv_to_dict(directors_movies_path), csv_to_dict(actors_movies_path)
    movies_genres = csv_to_dict(movies_genres_path)
    genres = get_genres(movies_genres)
    # create genres table
    genres_table(db, genres)
    movies_table(db, movies_genres)
    movies_genres_table(db, movies_genres)
    pid_table(db, actors_movies, 0)
    pid_table(db, directors_movies, 1)


# def main():
#     actors_movies_path, directors_movies_path = "actors_movies.csv", "directors_movies.csv"
#     movies_genres_path = "people_genres.csv"
#     directors_movies, actors_movies = csv_to_dict(directors_movies_path), csv_to_dict(actors_movies_path)
#     movies_genres = csv_to_dict(movies_genres_path)
#     genres = get_genres(movies_genres)
#     # create genres table
#     genres_table(genres)
#     movies_table(movies_genres)
#     movies_genres_table(movies_genres)
#     pid_table(actors_movies)
#     pid_table(directors_movies)

# if __name__ == '__main__':
#     main()
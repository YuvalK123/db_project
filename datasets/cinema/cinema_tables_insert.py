import mysql.connector as mysql
import csv
import json
import re

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


def convert_list_to_dict(array, to_replace=False):
    """
    :param array: to convert to dictionary
    :param to_replace: True to replace keys with values
    :return: dictionary from array
    """
    dic = dict(array)
    if not to_replace:
        return dic
    new_dic = {}
    for key, val in dic.items():
        new_dic[val] = key
    return new_dic


#########################################


def get_actors_movies(movies_genres):
    """
    gets actors, movies from shortYago csv file
    :return: dictionary from movie to genre, actors_movies dictionary {actor: [movies],...}
    """
    movies, actors_movies = set(), {}
    with open("D:/Db/3/shortYago2.csv", 'r', encoding='utf-16') as file:
        lines = file.readlines()
        for line in lines:
            if "actedIn" not in line:
                continue
            line = line.strip()
            sep_line, fin_line = line.split(',')[1:], []
            for word in sep_line:  # [actor, 'actedIn', movie]
                tmp = word.replace('<', '').replace('>', '').replace('_', ' ')  # remove dataset markings
                x = tmp.find("(")
                if x > 0:
                    tmp = tmp[:x - 2]  # remove brackets
                fin_line.append(tmp)
            movies.add(fin_line[2])  # add movie name to movies set
            if fin_line[0] not in actors_movies.keys():  # if actors not in
                actors_movies[fin_line[0]] = [fin_line[2]]
            else:
                actors_movies[fin_line[0]].append(fin_line[2])
            # ['Dirk Bogarde', 'actedIn', 'Accident']
    actors_movies_genres = assign_movies_genres(movies_genres, movies)
    return actors_movies_genres, actors_movies


def get_directors_movies(movies_genres):
    """
    :param yago_movies_genres: {movie_title : genre, ...}
    :param genres_id: {genre: int, ...}
    :param movies_genres: dictionary between movies and genres {movie: [genres], ...}
    :return: dictionary from director to movie {director: [movies], ...} and dictionary between movie to genre
    """
    scheme, movies_directors = [], {}
    directors_movies_set = set()
    # fills movies_directors = {director: [movies], ...}
    with open("D:/Db/3/directors.csv", 'r', encoding='utf-16') as directors_file:
        reader = csv.reader(directors_file, delimiter=',')
        for line in reader:
            line, fin_line = line[1:], []  # [director, 'Directed', movie]
            for word in line:
                tmp = word.replace('<', '').replace('>', '').replace('_', ' ')  # removes tokens from word
                x = tmp.find("(")
                if x > 0:
                    tmp = tmp[:x - 2]  # removes brackets from word
                fin_line.append(tmp)
            director, movie = fin_line[0], fin_line[2]
            directors_movies_set.add(movie)
            if director not in movies_directors.keys():
                movies_directors[director] = [movie]
            else:
                movies_directors[director].append(movie)

    # get genres for directors movies
    directors_movies_genres = assign_movies_genres(movies_genres, directors_movies_set)
    return directors_movies_genres, movies_directors
    '''
    for movie, genres in yago_movies_genres.items():
        movie_genres = []
        for genre in genres:
            movie_genres.append(genres_id[genre])
        dirs = []
        if movie in movies_directors.keys():
            dirs = movies_directors[movie]
        row = [movie, movie_genres]
        scheme.append(row)

    return scheme
    '''


def get_genres():
    """
    function gets movies genres
    :return: set of genres and dictionary between movies and genres {movie: [genres], ...}
    """
    file_name = "D:/Db/movies_metadata/movies_metadata.csv"
    with open(file_name, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        regex_txt, dic, genres = "name': '(.*?')", {}, set()
        next(reader, None)  # skip header
        for line in reader:
            title, string = line[8], json.loads(json.dumps(line[3]))
            if 'Written by' in string or 'Production' in string:  # skip unwanted lines
                continue
            tmps = re.findall(regex_txt, string)  # find all genres
            for t in tmps:  # iterate through the genres
                if 'TV' in t:  # tv movie is not a genre
                    continue
                genres.add(t[:-1])  # t = genre', t[:-1] = genre. adds genre to genres set
                if title in dic.keys():  # if movie is counted, add another genre to it.
                    dic[title].append(t[:-1])
                else:  # if movie isn't counted, add genre to it.
                    dic[title] = [t[:-1]]
        return dic, genres


def assign_movies_genres(movies_genres, movies_set):
    """
    function maps movies in dataset to their genre
    :param movies_genres: {movie: [genres], ...}
    :param movies_set: a set of movies from relevant dataset
    :return: dictionary from relevant movie dataset to it's genres. {movie: [genres], ...}
    """
    dic, keys = {}, movies_genres.keys()
    for movie in movies_set:
        dic[movie] = movies_genres[movie] if movie in keys else []
        # if movie in keys:
        #     dic[movie] = movies_genres[movie]
        # else:
        #     dic[movie] = []
    return dic


def movies_table(movies_list):
    """
    functions creates movies table
    :param movies_list: [(movie, "1, 5, ..."), ...]
    :return: None
    """
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=PASSWORD,
        database=DATABASE
    )
    cursor = db.cursor()
    max_movie_len = len(max(movies_list, key=lambda t: len(t[0]))[0]) + 10
    query = f"CREATE TABLE movies (id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
            f"movieName VARCHAR({max_movie_len}), genre VARCHAR(70));"
    cursor.execute(query)
    db.commit()
    query = "INSERT INTO movies (movieName, genre) VALUES (%s, %s);"
    cursor.executemany(query, movies_list)
    db.commit()
    db.disconnect()


def pid_table(movies, table_title="actors_movies"):
    """
    function creates table with the given title for (pid, movieId)
    :param movies: dictionary {person: [movies],...}
    :param table_title: title of table
    :return: None
    """
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=PASSWORD,
        database=DATABASE
    )
    cursor = db.cursor()
    query = f"CREATE TABLE {table_title} (pid MEDIUMINT, movieId MEDIUMINT);"
    cursor.execute(query)
    db.commit()

    # gets pid and movieId
    id_name_query = " SELECT id, movieName FROM movies "
    cursor.execute(id_name_query)
    movies_rows = cursor.fetchall()  # [(17521, 'Out of Bounds'), (17522, 'Slave Girls from Beyond Infinity'), ...]
    movies_rows = convert_list_to_dict(movies_rows, True)
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
            if movie not in movies_rows.keys():
                continue
            movie_id = movies_rows[movie]
            list_commit.append((person_id, movie_id))
    # insert values
    n = len(list_commit) // 5
    batches = [list_commit[i * n:(i + 1) * n] for i in range((len(list_commit) + n - 1) // n )]
    print("insert values to", table_title)
    for batch in batches:
        query = f"INSERT INTO {table_title} (pid, movieId) VALUES (%s, %s);"
        cursor.executemany(query, batch)
        db.commit()
    db.disconnect()


def genres_table(genres):
    """
    functions generates genres table
    :param genres: set of genres
    :return: None
    """
    print(genres)
    genres_db = [(genre,) for genre in genres]
    max_len = len(max(genres, key=len)) + 10  # , key=lambda t: len(t)) + 10
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=PASSWORD,
        database=DATABASE
    )
    cursor = db.cursor()
    query = f"CREATE TABLE genres (id TINYINT PRIMARY KEY NOT NULL AUTO_INCREMENT, genre VARCHAR({max_len}));"
    cursor.execute(query)
    db.commit()

    query = "INSERT INTO genres (genre) VALUES (%s)"
    cursor.executemany(query, genres_db)
    db.commit()
    db.disconnect()


def genres_to_id(genres_to_conv, genres_map):
    # db = mysql.connect(
    #     host="localhost",
    #     user="root",
    #     passwd=PASSWORD,
    #     database=DATABASE
    # )
    # cursor, final_genres = db.cursor(), []
    # genres_query = " SELECT id, genre FROM genres "
    # cursor.execute(genres_query)
    # genres = cursor.fetchall()  # [(1, 'western'), ...]
    # db.disconnect()
    # genres = convert_list_to_dict(genres, True)
    final_genres = []
    for genre in genres_to_conv:
        final_genres.append(genres_map[genre])
    return final_genres


def get_genres_id():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=PASSWORD,
        database=DATABASE
    )
    cursor, final_genres = db.cursor(), []
    genres_query = " SELECT id, genre FROM genres "
    cursor.execute(genres_query)
    genres = cursor.fetchall()  # [(1, 'western'), ...]
    db.disconnect()
    return convert_list_to_dict(genres, True)


def unite_movies(actors_movies, directors_movies):
    """
    function unites between 2 dictionaries of person -> genre
    :param actors_movies: {movie: [genres], ...}
    :param directors_movies: {movie: [genres], ...}
    :return: list of movies and genres, [(movie, "1, 5, ..."), ...]
    """
    final_list = []
    trythis = actors_movies.copy()
    trythis.update(directors_movies)
    genres_map = get_genres_id()

    def append_to_final(movie, genres):
        genres_ids = genres_to_id(genres, genres_map)
        genres_str = convert_list_to_string(genres_ids)
        final_list.append((movie, genres_str))

    for movie, genres in trythis.items():
        append_to_final(movie, genres)

    # for movie, genres in directors_movies.items():
    #     if movie in actors_movies.keys():
    #         continue
    #     append_to_final(movie, genres)

    return final_list


def main():
    print("genres")
    movies_genres, genres = get_genres()
    print("generates genres")
    genres_table(genres)
    print("movies")
    actors_movies_genres, actors_movies = get_actors_movies(movies_genres)
    directors_movies_genres, movies_directors = get_directors_movies(movies_genres)
    print("unites lists")
    movies_list = unite_movies(actors_movies_genres, directors_movies_genres)
    print("generate movies table")
    movies_table(movies_list)
    print("generate actors movies")
    pid_table(actors_movies, "actorsMovies")
    print("generate directors movies")
    pid_table(movies_directors, "directorsMovies")


if __name__ == '__main__':
    print("start")
    main()
    print("end")

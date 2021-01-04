from settings import *
import datetime
from dateutil.relativedelta import relativedelta
import random

def DatabaseError(error=None):
    return 'Database connection failed', 500


def datetime_tostring(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def get_from_option(option, country, amount):
    """
    :param option: born - 1 option or died - 0 option.
    :param country: of people who died/born
    :return:
    """
    if option == 1:
        query = f"SELECT Name FROM people_info WHERE DiedIn='{country}' ORDER BY RAND() LIMIT 1;"
        keyword = "has died"
    else:
        query = f"SELECT Name FROM people_info WHERE BornIn='{country}' ORDER BY RAND() LIMIT 1;"
        keyword = "was born"
    return query, keyword

def movies_record_to_list(cursor, movies_idx):
    movies = ",".join(movies_idx)
    acted_query = f"SELECT DISTINCT movies.movieName, genres.genre FROM movies, movies_genres, genres " \
                  f"WHERE movies.id = movies_genres.movieId AND movies_genres.genreId = genres.id and " \
                  f"movies.id IN ({movies}) ORDER BY movies.id;"
    cursor.execute(acted_query)
    record = cursor.fetchall()
    # print(d_record)
    if not record:
        return []
    dic = {}
    for r in record:
        if r[0] in dic.keys():
            dic[r[0]].append(r[1])
        else:
            dic[r[0]] = [r[1]]
    res = [{key: value} for key, value in dic.items()]
    return res


def id_to_country(country_id=None):
    if not country_id:
        return None
    query = f"SELECT Location FROM locations WHERE id={country_id}"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        return record[0]
    except Exception as e:
        print(e)
        return None


def country_to_id(country=None):
    if not country:
        return None
    query = f"SELECT id FROM locations WHERE Location='{country}';"
    print(query)
    try:
        cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        return record[0]
    except Exception as e:
        print(e)
        return None


def get_user_age(uid):
    yeardays = 365.2425
    age = -1
    try:
        cursor = db.cursor()
        query = f"SELECT age FROM users WHERE id={uid}"
        cursor.execute(query)
        age = cursor.fetchone()
        if age:
            today, age = datetime.date.today(), age[0]
            age = (today - age).days/yeardays
    except Exception as e:
        print(e)
    return str(age)
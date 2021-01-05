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


def countries_to_ids(countries):
    """

    :param countries: union of locations strings
    :return: list of ids
    """
    if not countries:
        return None
    idx = []
    locations = ",".join([f"'{x}'" for x in countries])
    query = f"SELECT id FROM locations WHERE location IN ({locations});"
    try:
        cursor = db.cursor()
        rows = cursor.execute(query)
        if not rows:
            return []
        records = cursor.fetchall()
        if records:
            idx = [x[0] for x in records]
    except Exception as e:
        print(e)
    return idx


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


def filter_countries(countries_idx, uid, table="user_locations"):
    """

    :param countries_idx: union of countries indices
    :param uid: user id.
    :param table: table with location and uid field
    :return: list of countries idx that don't exist in table
    """
    query, idx = f"SELECT location FROM {table} WHERE uid={uid}", None
    try:
        cursor = db.cursor()
        rows = cursor.execute(query)
        if not rows:
            return []
        records = cursor.fetchall()
        if not records:
            return []
        idx = [x[0] for x in records]
    except Exception as e:
        print(e)
    if not idx:
        return []
    ret = [x for x in countries_idx if x not in idx]
    return ret


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


def update_hints(uid, amount, cursor=None, relative_amount=False):
    if relative_amount:
        query = f"SELECT hints FROM games WHERE uid={uid}"
        if not cursor:
            cursor = db.cursor()
        rows = cursor.execute(query)
        record = cursor.fetchone()
        print(record)
        if record:
            hints = record[0]
            amount += hints
    print(amount)
    return update_query(table="games", fields={'hints': amount}, where={'uid': uid}, cursor=cursor)


def update_query(query=None, table=None, fields=None, where=None, cursor=None):
    """
    :param cursor: db cursor
    :param query: full query to execute
    :param table: if not query, table to update
    :param fields: if not query, fields dictionary - {'field name': 'field value', ...}
    :param where: if not query, where clause dictionary {'field name': 'field value', ...}
    :return: number of row affected
    """

    if not query:
        # build query
        condition = table is not None and fields is not None
        if not condition:
            print(table, fields)
            return -1
        query = f"UPDATE {table} SET "
        fields_clause = [f"{key}='{val}'" for key, val in fields.items()]
        query += ", ".join(fields_clause)
        if where:
            query += " WHERE "
            where_clause = [f"{key}='{val}'" for key, val in where.items()]
            query += ", ".join(where_clause)
    print(query)
    rows = 0
    try:
        if not cursor:
            cursor = db.cursor()
        rows = cursor.execute(query)
        db.commit()
    except Exception as e:
        print(e)
    return rows


def insert_query(query, cursor=None):
    pass


def select_query(query, cursor=None, is_many=True):
    """
    :param query: any select query
    :param cursor: db cursor
    :param is_many: to fetch many or one record
    :return: records from select query
    """
    try:
        if not cursor:
            cursor = db.cursor()
        rows = cursor.execute(query)
        if not rows:
            return tuple()
        exec_f = cursor.fetchall
        if not is_many:
            exec_f = cursor.fetchone
        records = exec_f()
        return records
    except Exception as e:
        print(e)
    return tuple()

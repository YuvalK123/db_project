from settings import *
import datetime
from dateutil.relativedelta import relativedelta
import random


def DatabaseError(error=None):
    return 'Database connection failed', 500


def datetime_tostring(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def get_hints(country, amount, cursor=None):
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
    except Exception as e:
        return DatabaseError(e)
    queries = {"born": [], "died": [], "rests": []}
    died_count = count_records(table="people_info", where=f"DiedIn='{country}'", cursor=cursor)
    born_count = count_records(table="people_info", where=f"BornIn='{country}'", cursor=cursor)
    if born_count:
        query = f"SELECT Name FROM people_info WHERE BornIn='{country}' ORDER BY RAND() LIMIT {amount};"
        born = select_query(query=query, is_many=True, cursor=cursor)
        born = [f"{x[0]} was born there" for x in born]
        queries["born"] = born
    if died_count:
        query = f"SELECT Name FROM people_info WHERE DiedIn='{country}' ORDER BY RAND() LIMIT {amount};"
        died = select_query(query=query, is_many=True, cursor=cursor)
        died = [f"{x[0]} died there" for x in died]
        queries["died"] = died
    if born_count + died_count < amount:
        rests_count = count_records(table="restaurants", where=f"city_id={country}", cursor=cursor)
        if rests_count:
            rests_hints = []
            query = f"SELECT name, COUNT(name) AS c FROM restaurants WHERE city_id = {country} " \
                    f"GROUP BY name ORDER BY c DESC;"
            rests = select_query(query=query, is_many=True, cursor=cursor)
            if rests:
                for rest in rests:
                    hint = f"{rest[0]} has {rest[1]} restaurants there"
                    rests_hints.append(hint)
            rests_hints.append(f"There is a total of {rests_count} restaurants there")
            queries["rests"] = rests_hints
    if is_new:
        if cursor:
            cursor.close()
    return queries


def movies_record_to_list(movies_idx, cursor=None):
    """
    function gets movies indices, and return array of {movie:[genres]}
    :param movies_idx: union of movie indices
    :param cursor: of db
    :return: array of {movie:[genres]}
    """
    movies = ",".join(str(v) for v in movies_idx)
    acted_query = f"SELECT DISTINCT movies.movieName, genres.genre FROM movies, movies_genres, genres " \
                  f"WHERE movies.id = movies_genres.movieId AND movies_genres.genreId = genres.id and " \
                  f"movies.id IN ({movies}) ORDER BY movies.id;"
    records = select_query(acted_query, cursor=cursor, is_many=True)
    if not records:
        return []
    dic = {}
    for r in records:
        if r[0] in dic.keys():
            dic[r[0]].append(r[1])
        else:
            dic[r[0]] = [r[1]]
    res = [{key: value} for key, value in dic.items()]
    return res


def id_to_country(cursor=None, country_id=None):
    """
    function converts id to country string
    :param cursor: db cursor
    :param country_id: country id.
    :return:
    """
    if not country_id:
        return None
    query = f"SELECT Location FROM locations WHERE id={country_id}"
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        if is_new:
            if cursor:
                cursor.close()
        return record[0]
    except Exception as e:
        print(e)
        if is_new:
            if cursor:
                cursor.close()
        return None


def countries_to_ids(countries, cursor=None):
    """

    :param countries: union of locations strings
    :return: list of ids
    """
    is_new = False
    if not countries:
        return None
    idx = []
    locations = ",".join([f"'{x}'" for x in countries])
    query = f"SELECT id FROM locations WHERE location IN ({locations});"
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        # cursor = db.cursor()
        rows = cursor.execute(query)
        if not rows:
            if is_new:
                if cursor:
                    cursor.close()
            return []
        records = cursor.fetchall()
        if records:
            idx = [x[0] for x in records]
    except Exception as e:
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return idx


def country_to_id(cursor, country=None):
    if not country:
        return None
    query = f"SELECT id FROM locations WHERE Location='{country}';"
    print(query)
    try:
        cursor.execute(query)
        record = cursor.fetchone()
        return record[0]
    except Exception as e:
        print(e)
        return None


def filter_countries(countries_idx, uid, cursor=None, table="user_locations"):
    """
    :param countries_idx: union of countries indices
    :param uid: user id.
    :param cursor: db cursor
    :param table: table with location and uid field
    :return: list of countries idx that don't exist in table
    """
    is_new = False
    query, idx = f"SELECT location FROM {table} WHERE uid={uid}", None
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
        records = cursor.fetchall()
        if not records:
            if is_new:
                if cursor:
                    cursor.close()
            return countries_idx
        idx = [x[0] for x in records]
    except Exception as e:
        print(e)
        if is_new:
            if cursor:
                cursor.close()
        return []
    ret = [x for x in countries_idx if x not in idx]
    if is_new:
        if cursor:
            cursor.close()
    return ret


def update_hints(uid, amount, cursor=None, relative_amount=False):
    is_new = False
    if relative_amount:
        amount = int(amount)
        query = f"SELECT hints FROM games WHERE uid={uid}"
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
        record = cursor.fetchone()
        if record:
            hints = record[0]
            amount += hints
    where = f"WHERE uid={uid}"
    val = update_query(table="games", fields={'hints': amount}, where=where, cursor=cursor)
    if is_new:
        if cursor:
            cursor.close()
    return val


def update_query(query=None, table=None, fields=None, where=None, cursor=None):
    """
    :param cursor: db cursor
    :param query: full query to execute
    :param table: if not query, table to update
    :param fields: if not query, fields dictionary - {'field name': 'field value', ...}
    :param where: if not query, where clause string starting with WHERE
    :return: number of row affected, -1 if invalid input
    """
    rows = 0
    is_new = False
    if not query:
        # build query
        condition = table is not None and fields is not None
        if not condition:
            return -1
        query = f"UPDATE {table} SET "
        fields_clause = [f"{key}='{val}'" for key, val in fields.items()]
        query += ", ".join(fields_clause)
        if where:
            query += " " + where
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return rows


def insert_query(query=None, table=None, fields=None, execmany=None, cursor=None):
    """
    :param query: full query to execute
    :param table: if not query, table to update
    :param fields: if not query, fields dictionary - {'field name': 'field value', ...}
    :param execmany: union of tuples of values to insert
    :param cursor: db cursor
    :return: number of row affected, -1 if invalid input
    """
    is_new = False
    if not query:
        # build query
        condition = table is not None and fields is not None
        if not condition:
            return -1
        query = f"INSERT INTO {table} ("
        query += ", ".join(fields.keys())
        query += ") VALUES ("
        if not execmany:
            query += ",".join([f"'{x}'" for x in fields.values()])
        else:
            length = len(fields.keys())
            vals = ["%s" for i in range(length)]
            query += ", ".join(vals)
        query += ");"
    rows = 0
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        if execmany:
            rows = cursor.executemany(query, execmany)
        else:
            rows = cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return rows


def delete_query(query, cursor=None, to_commit=True):
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
        if to_commit:
            db.commit()
    except Exception as e:
        db.rollback()
        if is_new:
            if cursor:
                cursor.close()
        return -1
    if is_new:
        if cursor:
            cursor.close()
    return rows


def select_query(query, cursor=None, is_many=True):
    """
    :param query: any select query
    :param cursor: db cursor
    :param is_many: to fetch many or one record
    :return: records from select query
    """
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
        if not rows:
            return tuple()
        exec_f = cursor.fetchall
        if not is_many:
            exec_f = cursor.fetchone
        records = exec_f()
        if is_new:
            if cursor:
                cursor.close()
        return records
    except Exception as e:
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return tuple()


def check_if_admin(uid, cursor=None):
    query = f"SELECT * FROM admins WHERE uid={uid}"
    rows = 0
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        rows = cursor.execute(query)
    except Exception as e:
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return rows != 0


def count_records(table: str, cursor=None, where=None):
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
        # build query
        query = f"SELECT COUNT(*) FROM {table}"
        if where:
            query += " WHERE " + where
        cursor.execute(query)
        rows = cursor.fetchone()
        if rows:
            rows = rows[0]
        if is_new:
            if cursor:
                cursor.close()
        return rows
    except Exception as e:
        print(e)
    if is_new:
        if cursor:
            cursor.close()
    return -1


def add_location(location: str, cursor=None):
    """

    :param location: string name of place
    :param cursor: database cursor
    :return: id of place in db
    """
    is_new = False
    try:
        if not cursor:
            is_new = True
            cursor = db.cursor()
    except:
        return -1
    record = select_query(query=f"SELECT id FROM locations WHERE LOWER(location)='{location.strip().lower()}'",
                          cursor=cursor, is_many=False)
    if record:
        if is_new:
            if cursor:
                cursor.close()
        return record[0]
    query = f"INSERT INTO locations (location) VALUES ('{location.strip()}');"
    rows = insert_query(query=query, cursor=cursor)
    try:
        country_id = cursor.lastrowid
    except Exception as e:
        country_id = -1
    if is_new:
        if cursor:
            cursor.close()
    return country_id

from settings import *
from datetime import datetime
import random

def DatabaseError(error):
    return 'Database connection failed', 500


def get_from_option(option, country):
    if option == 1:
        query = f"SELECT Name, DiedIn FROM people_info WHERE DiedIn='{country} ' ORDER BY RAND() LIMIT 1;"
        keyword = "has died"
    else:
        query = f"SELECT Name, BornIn FROM people_info WHERE BornIn='{country} ' ORDER BY RAND() LIMIT 1;"
        keyword = "was born"
    return query, keyword

i = 0
@app.route('/hint')
def get_hint():
    options = ["bornin, diedin, restaurant"]
    global i
    print(i)
    i += 1
    try:
        cursor = db.cursor()
        option, country = random.randint(1, 2), request.args.get('country')
        query, keyword = get_from_option(option, country)
        cursor.execute(query)
        result = cursor.fetchall()
        print("result", result)
        if len(result) > 0:
            record = result[0]
            result = f"{record[0]} {keyword} there"
        else:
            query, keyword = get_from_option((option % 2) + 1, country)
            cursor.execute(query)
            result = cursor.fetchone()
            print("result", result)
            if len(result) > 0:
                record = result[0]
                result = f"{record[0]} was {keyword} there"
        return result
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/get_country')
def get_random_country():
    print("random")
    query = "SELECT location FROM locations ORDER BY RAND() LIMIT 1"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        country = cursor.fetchone()
        if len(country) > 0:
            return country[0]
        return "fail"
    except Exception as e:
        return DatabaseError(e)


@app.route('/get_people')
def get_all_related():
    print("get people")
    country = request.args.get('country')
    born_query = f"SELECT Name FROM people_info WHERE BornIn='{country} ';"
    died_query = f"SELECT Name FROM people_info WHERE DiedIn='{country} ';"
    try:
        cursor = db.cursor()
        cursor.execute(born_query)
        born_country = cursor.fetchall()
        born_country = [x[0] for x in born_country]
        cursor.execute(died_query)
        died_country = cursor.fetchall()
        died_country = [x[0] for x in died_country]
        print(died_country)
        print("cool")
        b = ",".join(born_country)
        d = ",".join(died_country)
        ret = str(b + "|||" + d)
        print(ret)
        return ret
    except Exception as e:
        print(e)
        return DatabaseError(e)


@app.route('/users', methods=['GET', 'POST'], )
def users():
    if request.method == 'POST':
        # add user
        pass
    else:
        try:
            arg1 = request.args.get('user')
            print(arg1)
        except Exception as e:
            print("e", e)
    print('a')
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    print("index")
    if request.method == 'POST':
        print(request)
        task_content = request.form['content']
        try:
            cursor = db.cursor()
            return redirect('/')
        except Exception as e:
            print(e)
            return render_template('index.html')
            # return 'There was an issue adding the task'
    else:
        return render_template('index.html')


app.run(debug=True, port=PORT)

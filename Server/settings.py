from flask import Flask, render_template, url_for, request, redirect, Response
from flaskext.mysql import MySQL
# from flask_sqlalchemy import SQLAlchemy
import yaml
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
PORT = 3000
# db_params = yaml.load(open('db.yaml'))
# PASSWORD = db_params['mysql_password']
# DATABASE = db_params['mysql_db']
# USER = db_params['mysql_user']
# HOST = db_params['mysql_host']
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
# db = SQLAlchemy(app)

mysql = MySQL()
db_params = yaml.load(open('db.yaml'))
app.config['MYSQL_DATABASE_HOST'] = db_params['mysql_host']
app.config['MYSQL_DATABASE_USER'] = db_params['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db_params['mysql_password']
app.config['MYSQL_DATABASE_DB'] = db_params['mysql_db']
mysql.init_app(app)
db = mysql.connect()



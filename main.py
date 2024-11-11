from functools import wraps

from flask import request, render_template, redirect, session, url_for
from flask import Flask
import sqlite3
import os
app = Flask(__name__)
app.secret_key = '45y9thj5k6nhy5k6jnh'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB_Rent():

    def __init__(self, file_name):
        self.con = sqlite3.connect(file_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()

def check_login():
    if session.get('user_id') is None:
        redirect('login')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def start_app():
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute('''SELECT id from user where login = ? and password = ?''', (login, password))
            user = db_cur.fetchone()
            if user:
                session['user_id'] = user['id']
                return redirect('/profile')
            else:
                return ('Wrong login/password')





@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    if request.method == 'POST':
        session.pop('user_id', None)
        return redirect('/login')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        with DB_Rent('identifier.sqlite') as db_cur:
            form_data = request.form
            db_cur.execute("""INSERT INTO user (login, password, full_name, ipn, passport, contacts, photo) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                form_data['login'], form_data['password'], form_data['full_name'], form_data['ipn'],
                form_data['passport'], form_data['contacts'], form_data['photo'],

                       )
                           )
        return redirect('/login')

@app.route("/profile", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@login_required
def profile_user():
    if request.method == 'GET':
        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute(f'''SELECT * FROM user WHERE id = {session["user_id"]}''')
            user_data = db_cur.fetchall()
            print(user_data)
        return render_template('user.html', user_data=user_data)
    if request.method == 'PUT':
        return 'PUT -> /profile'
    if request.method == 'PATCH':
        return 'PATCH -> /profile'
    if request.method == 'DELETE':
        return 'DELETE -> /profile/user'

@app.route("/profile/my_items", methods=['GET'])
@login_required
def my_items():
    if request.method == 'GET':
        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute(f'''SELECT * FROM item WHERE owner = {session["user_id"]} ''')
            my_items = db_cur.fetchall()
            print(my_items)
        return render_template('items.html', items=my_items)


@app.route("/profile/my_contracts", methods=['GET'])
@login_required
def my_contracts():
    if request.method == 'GET':
        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute(f'''SELECT * FROM contract WHERE leaser = {session["user_id"]} OR taker = {session["user_id"]}''')
            my_contracts = db_cur.fetchall()
            print(my_contracts)
        return render_template('contracts_tbl.html', contracts=my_contracts)


@app.route("/profile/add_item", methods=['GET'])
@login_required
def add_item():
    if request.method == 'GET':
        return render_template('add_item.html')


@app.route("/profile/favourites", methods=['GET', 'POST', 'PATCH', 'DELETE'])
@login_required
def profile_favourites():
    if request.method == 'POST':
        return 'POST -> /profile/favourites'
    if request.method == 'GET':
        return 'GET -> /profile/favourites'
    if request.method == 'PATCH':
        return 'PATCH -> /profile/favourites'
    if request.method == 'DELETE':
        return 'DELETE -> /profile/favourites'

@app.route("/profile/favourites/<favourite_id>", methods=['DELETE'])
@login_required
def profile_favourites_id(favourite_id):
    if request.method == 'DELETE':
        return 'DELETE -> profile/favourites/<favourite_id>'

@app.route("/items", methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute('SELECT * FROM item')
            get_items = db_cur.fetchall()
        return render_template('items.html', items=get_items)

    if request.method == 'POST':
        if session.get('user_id') is None:
            return redirect('login')

        with DB_Rent('identifier.sqlite') as db_cur:
            form_data = request.form
            db_cur.execute("""INSERT INTO item (name, description, price_hour, price_day, price_week, price_month, photo, owner) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                           (
                               form_data['name'], form_data['description'], form_data['price_hour'], form_data['price_day'],
                               form_data['price_week'], form_data['price_month'], form_data['photo'], session["user_id"],
                           )
                           )
        return redirect('/profile/my_items')


@app.route("/items/<item_id>", methods=['GET', 'DELETE'])
def item_id(item_id):
    if request.method == 'GET':
        return 'GET -> /items/<item_id>'
    if request.method == 'DELETE':
        return 'DELETE -> /items/<item_id>'


@app.route("/leasers", methods=['GET'])
@login_required
def leasers():
    if request.method == 'GET':
        return 'GET -> /leasers'

@app.route("/leasers/<leaser_id>", methods=['GET'])
def leaser_id(leaser_id):
    if request.method == 'GET':
        return 'GET -> /leasers/<leaser_id>'

@app.route("/contracts", methods=['GET', 'POST'])
@login_required
def contracts():
    if request.method == 'GET':
        with DB_Rent('identifier.sqlite') as db_cur:
            db_cur.execute('SELECT * FROM contract')
            get_contracts = db_cur.fetchall()
        return render_template('contracts_tbl.html', contracts=get_contracts)
    if request.method == 'POST':
        return 'POST -> /contracts'


@app.route("/contracts/<contract_id>", methods=['GET', 'PUT','PATCH'])
@login_required
def contract_id(contract_id):
    if request.method == 'PUT':
        return 'PUT -> /contracts/<contract_id>'
    if request.method == 'GET':
        return 'GET -> /contracts/<contract_id>'
    if request.method == 'PATCH':
        return 'PATCH -> /contracts/<contract_id>'

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        return 'POST -> /search'
    if request.method == 'GET':
        return 'GET -> /search'

# @app.route("/complain", methods=['POST'])
# def complain():
#     if request.method == 'POST':
#         return 'POST -> /complain'

@app.route("/compare", methods=['GET', 'PUT', 'PATCH'])
def compare():
    if request.method == 'PUT':
        return 'PUT -> /compare'
    if request.method == 'GET':
        return 'GET -> /compare'
    if request.method == 'PATCH':
        return 'PATCH -> /compare'

if __name__ == '__main__':
    app.run()

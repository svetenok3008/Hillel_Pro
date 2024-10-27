from flask import request, render_template

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'POST -> /login'
    if request.method == 'GET':
        return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST', 'DELETE'])
def logout():
    if request.method == 'POST':
        return 'POST -> /logout'
    if request.method == 'GET':
        return 'GET -> /logout'
    if request.method == 'DELETE':
        return 'DELETE -> /logout'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'POST -> /register'
    if request.method == 'GET':
        return 'GET -> /register'

@app.route("/profile/user", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def profile_user():
    if request.method == 'PUT':
        return 'PUT -> /profile/user'
    if request.method == 'GET':
        return 'GET -> /profile/user'
    if request.method == 'PATCH':
        return 'PATCH -> /profile/user'
    if request.method == 'DELETE':
        return 'DELETE -> /profile/user'


@app.route("/profile/favourites", methods=['GET', 'POST', 'PATCH', 'DELETE'])
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
def profile_favourites_id(favourite_id):
    if request.method == 'DELETE':
        return 'DELETE -> profile/favourites/<favourite_id>'

@app.route("/items", methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        return 'POST -> /items'
    if request.method == 'GET':
        return 'GET -> /items'

@app.route("/items/<item_id>", methods=['GET', 'DELETE'])
def item_id(item_id):
    if request.method == 'DELETE':
        return 'DELETE -> /items/<item_id>'
    if request.method == 'GET':
        return 'GET -> /items/<item_id>'

@app.route("/leasers", methods=['GET'])
def leasers():
    if request.method == 'GET':
        return 'GET -> /leasers'

@app.route("/leasers/<leaser_id>", methods=['GET'])
def leaser_id(leaser_id):
    if request.method == 'GET':
        return 'GET -> /leasers/<leaser_id>'

@app.route("/contracts", methods=['GET', 'POST'])
def contracts():
    if request.method == 'POST':
        return 'POST -> /contracts'
    if request.method == 'GET':
        return 'GET -> /contracts'

@app.route("/contracts/<contract_id>", methods=['GET', 'PUT','PATCH'])
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

@app.route("/complain", methods=['POST'])
def complain():
    if request.method == 'POST':
        return 'POST -> /complain'

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

# TODO: error handling on all functions
# TODO: change all stored class attributes to their correct type instead of all being of type str
# ------------------------------------------------------------------------------ #
from flask import Flask, request, session, json, jsonify, make_response
import jsonpickle
app = Flask(__name__)
# used for sessions, generated using:
# python -c 'import os; print(os.urandom(16))'
app.secret_key = '??\9-?_YL?0q'
# ------------------------------------------------------------------------------ #
class Address:
    def __init__(self, street, city, state, zip):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Customer:
    def __init__(self, id, username, address):
        self.id = id
        self.username = username
        self.address = address

class Order:
    def __init__(self, id, petId, quantity, shipDate, status, complete):
        self.id = id
        self.petId = petId
        self.quantity = quantity
        self.shipDate = shipDate
        self.status = status
        self.complete = complete

class Pet:
    def __init__(self, id, name, category, photoUrls, tags, status):
        self.id = id
        self.name = name
        self.category = category
        self.photoUrls = photoUrls
        self.tags = tags
        self.status = status

class Tag:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class User:
    def __init__(self, id, username, firstName, lastName, email, password, phone, userStatus):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.userStatus = userStatus
# ------------------------------------------------------------------------------ #
# static storage dictionaries (not connecting to a database)
# key: unique id, value: object instance
_orders = {}
_pets = {}
# key: unique username, value: object instance
_users = {}
# user that is currently signed into a session
global _current_user
_current_user = 'nobody'
# used to parse stored class data in JSON response
p = jsonpickle.Pickler()
# ------------------------------------------------------------------------------ #
# NOTE: URL formatting: http://127.0.0.1:5000/[route_path]?arg1=val1&arg2=val2 ...
# TODO: return JSON not str
# TODO: accept JSON input not just args in URL
@app.route('/pet', methods=['PUT', 'POST'])
def update_pet():
    id = request.args.get('id')
    name = request.args.get('name')
    category = request.args.get('category')
    photoUrls = request.args.get('photoUrls').split(',') # required
    # NOTE: separate tag args by commas in URL
    tags = request.args.get('tags').split(',') # required
    status = request.args.get('status')
    # _pets dictionary functions as desired without consideration of HTTP request method
    new_pet = Pet(id, name, category, photoUrls, tags, status)
    _pets[id] = new_pet
    return str(p.flatten(new_pet))

@app.route('/pet/findByStatus', methods=['GET'])
def find_by_status():
    status = request.args.get('status')
    status_matches = []
    for pet in _pets.values():
        if pet.status == status:
            status_matches.append(pet)
    return str(p.flatten(status_matches))

@app.route('/pet/findByTags', methods=['GET'])
def find_by_tags():
    tags = request.args.get('tags').split(',')
    tag_matches = []
    for tag in tags:
        for pet in _pets.values():
            if pet not in tag_matches and tag in pet.tags:
                tag_matches.append(pet)
    return str(p.flatten(tag_matches))

@app.route('/pet/<petId>', methods=['GET', 'POST', 'DELETE'])
def update_pet_by_id(petId):
    name = request.args.get('name')
    status = request.args.get('status')
    # find pet by id
    if request.method == 'GET':
        pet = _pets[petId]
        return str(p.flatten(pet))
    # updates a pet in the store with form data
    elif request.method == 'POST':
        _pets[petId].name = name
        _pets[petId].status = status
        return str(p.flatten(_pets[petId]))
    # deletes a pet
    else:
        _pets.pop(petId)
        return 'Pet ' + str(petId) + ' was successfully removed from the database.'

@app.route('/pet/<petId>/<uploadImage>', methods=['POST'])
def upload_image(petId, uploadImage):
    _pets[petId].photoUrls.append(uploadImage)
    return 'Image ' + str(uploadImage) + ' was successfully added to the database for pet ' + str(petId) + '.'
# ------------------------------------------------------------------------------ #
@app.route('/store/inventory', methods=['GET'])
def inventory():
    # _statuses = ['available', 'pending', 'sold']
    status_dict = {}
    status_dict['available'] = 0
    status_dict['pending'] = 0
    status_dict['sold'] = 0
    for pet in _pets.values():
        status_dict[pet.status] += 1
    return str(p.flatten(status_dict))

@app.route('/store/order', methods=['POST'])
def order():
    id = request.args.get('id')
    petId = request.args.get('petId')
    quantity = request.args.get('quantity')
    shipDate = request.args.get('shipDate')
    status = request.args.get('status')
    complete = request.args.get('complete')

    new_order = Order(id, petId, quantity, shipDate, status, complete)
    _orders[id] = new_order
    return str(p.flatten(new_order))

@app.route('/store/order/<orderId>', methods=['GET', 'DELETE'])
def order_by_id(orderId):
    # find purchase order by id
    if request.method == 'GET':
        order = _orders[orderId]
        return str(p.flatten(order))
    # delete purchase order by id
    else:
        _orders.pop(orderId)
        return 'Order ' + str(orderId) + ' has been successfully deleted from the database.'
# ------------------------------------------------------------------------------ #
@app.route('/user', methods=['POST'])
def create_user():
    id = request.args.get('id')
    username = request.args.get('username')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    email = request.args.get('email')
    password = request.args.get('password')
    phone = request.args.get('phone')
    userStatus = request.args.get('userStatus')

    new_user = User(id, username, firstName, lastName, email, password, phone, userStatus)
    _users[username] = new_user
    return str(p.flatten(new_user))

# TODO: implement
# @app.route('/user/createWithList', methods=['POST'])
# def create_with_list(user_arr):

@app.route('/user/login', methods=['GET'])
def login():
    global _current_user
    username = request.args.get('username')
    password = request.args.get('password')
    if username in _users and _users[username].password == password:
        _current_user = username
        return username + ' was successfully logged in.'
    return 'Login failed. Check credentials and try again.'

@app.route('/user/logout', methods=['GET'])
def logout():
    global _current_user
    logged_out_user = _current_user
    if _current_user != 'nobody':
        _current_user = 'nobody'
        return logged_out_user + ' was successfully logged out.'
    return 'Logout failed. Nobody is currently logged in.'

@app.route('/user/<username>', methods=['GET', 'PUT', 'DELETE'])
def update_user(username):
    global _current_user
    id = request.args.get('id')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    email = request.args.get('email')
    password = request.args.get('password')
    phone = request.args.get('phone')
    userStatus = request.args.get('userStatus')

    # get user by user name
    if request.method == 'GET':
        user = _users[username]
        return str(p.flatten(user))
    # update user
    elif request.method == 'PUT':
        if _current_user == username:
            _users[username] = User(id, username, firstName, lastName, email, password, phone, userStatus)
            return str(p.flatten(_users[username]))
        return 'You do not have permission to update this user\'s account.'
    # delete user
    else:
        if _current_user == username:
            _users.pop(username)
            return username + '\'s account was successfully deleted.'
        return 'You do not have permission to delete this user\'s account.'
# ------------------------------------------------------------------------------ #

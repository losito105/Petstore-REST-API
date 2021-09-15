# ------------------------------------------------------------------------------ #
from flask import Flask, request, abort
import jsonpickle
app = Flask(__name__)
# ------------------------------------------------------------------------------ #
class Address:
    def __init__(self, street, city, state, zip):
        self.street = str(street)
        self.city = str(city)
        self.state = str(state)
        self.zip = str(zip)

class Customer:
    def __init__(self, id, username, address):
        self.id = int(id)
        self.username = str(username)
        self.address = address # instance of class Address

class Order:
    def __init__(self, id, petId, quantity, shipDate, status, complete):
        self.id = int(id)
        self.petId = int(petId)
        self.quantity = int(quantity)
        self.shipDate = str(shipDate)
        self.status = str(status)
        self.complete = bool(complete)

class Pet:
    def __init__(self, id, name, category, photoUrls, tags, status):
        self.id = int(id)
        self.name = str(name)
        self.category = str(category)
        self.photoUrls = photoUrls # list of strings
        self.tags = tags # list of strings
        self.status = str(status)

class User:
    def __init__(self, id, username, firstName, lastName, email, password, phone, userStatus):
        self.id = int(id)
        self.username = str(username)
        self.firstName = str(firstName)
        self.lastName = str(lastName)
        self.email = str(email)
        self.password = str(password)
        self.phone = str(phone)
        self.userStatus = int(userStatus)
# ------------------------------------------------------------------------------ #
# static storage dictionaries (not connecting to a database)
# key: unique id, value: object instance
_orders = {}
_pets = {}
# key: unique username, value: object instance
_users = {}
# user that is currently signed in
global _current_user
_current_user = 'nobody'
# used to parse stored class data in JSON response
p = jsonpickle.Pickler()
# status enums for error checking
_pet_status_enum = ['available', 'pending', 'sold']
_order_status_enum = ['placed', 'approved', 'delivered']
# ------------------------------------------------------------------------------ #
@app.route('/pet', methods=['PUT', 'POST'])
def update_pet():
    pet_info = request.get_json()
    id = pet_info['id']
    name = pet_info['name']
    category = pet_info['category']
    photoUrls = pet_info['photoUrls']
    tags = pet_info['tags']
    status = pet_info['status']
    if photoUrls == None or tags == None or id < 0 or status not in _pet_status_enum:
        abort(405)
    # _pets dictionary functions as desired without consideration of HTTP request method
    new_pet = Pet(id, name, category, photoUrls, tags, status)
    _pets[id] = new_pet
    return str(p.flatten(new_pet))

@app.route('/pet/findByStatus', methods=['GET'])
def find_by_status():
    status = request.args.get('status')
    if status not in _pet_status_enum:
        abort(400)

    status_matches = []
    for pet in _pets.values():
        if pet.status == status:
            status_matches.append(pet)
    return str(p.flatten(status_matches))

@app.route('/pet/findByTags', methods=['GET'])
def find_by_tags():
    # considering all tags valid
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
    petId_num = int(petId) # quick fix, not ideal
    if petId_num < 0:
        abort(400)
    elif petId_num not in _pets:
        abort(404)
    # find pet by id
    if request.method == 'GET':
        pet = _pets[petId_num]
        return str(p.flatten(pet))
    # updates a pet in the store with form data
    elif request.method == 'POST':
        _pets[petId_num].name = name
        _pets[petId_num].status = status
        return str(p.flatten(_pets[petId_num]))
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
    # NOTE: this should be global for efficiency
    status_dict = {}
    status_dict['available'] = 0
    status_dict['pending'] = 0
    status_dict['sold'] = 0
    for pet in _pets.values():
        status_dict[pet.status] += 1
    return str(p.flatten(status_dict))

@app.route('/store/order', methods=['POST'])
def order():
    order_info = request.get_json()
    id = order_info['id']
    petId = order_info['petId']
    quantity = order_info['quantity']
    shipDate = order_info['shipDate']
    status = order_info['status']
    complete = order_info['complete']
    if id < 0 or petId < 0 or quantity <= 0 or status not in _order_status_enum:
        abort(405)
    elif complete != 'True' and complete != 'False':
        abort(405)

    new_order = Order(id, petId, quantity, shipDate, status, complete)
    _orders[id] = new_order
    return str(p.flatten(new_order))

@app.route('/store/order/<orderId>', methods=['GET', 'DELETE'])
def order_by_id(orderId):
    if orderId < 0 or orderId > 1000: # see Swagger Petstore docs
        abort(400)
    order = _orders[orderId]
    if order == None:
        abort(404)
    # find purchase order by id
    if request.method == 'GET':
        return str(p.flatten(order))
    # delete purchase order by id
    else:
        _orders.pop(orderId)
        return 'Order ' + str(orderId) + ' has been successfully deleted from the database.'
# ------------------------------------------------------------------------------ #
@app.route('/user', methods=['POST'])
def create_user():
    user_info = request.get_json()
    id = user_info['id']
    username = user_info['username']
    firstName = user_info['firstName']
    lastName = user_info['lastName']
    email = user_info['email']
    password = user_info['password']
    phone = user_info['phone']
    userStatus = user_info['userStatus']
    if id < 0:
        abort(400)

    new_user = User(id, username, firstName, lastName, email, password, phone, userStatus)
    _users[username] = new_user
    return str(p.flatten(new_user))

@app.route('/user/createWithList', methods=['POST'])
def create_with_list():
    user_lst = request.get_json()
    for user in user_lst:
        id = user['id']
        username = user['username']
        firstName = user['firstName']
        lastName = user['lastName']
        email = user['email']
        password = user['password']
        phone = user['phone']
        userStatus = user['userStatus']
        if id < 0:
            abort(400)

        new_user = User(id, username, firstName, lastName, email, password, phone, userStatus)
        _users[username] = new_user
    return str(p.flatten(user_lst))

@app.route('/user/login', methods=['GET'])
def login():
    global _current_user
    username = request.args.get('username')
    password = request.args.get('password')
    if username in _users and _users[username].password == password:
        _current_user = username
        return username + ' was successfully logged in.'
    else:
        abort(400) # bad credentials

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
    user = _users[username]
    if user == None:
        abort(404)

    # get user by user name
    if request.method == 'GET':
        return str(p.flatten(user))
    # update user
    elif request.method == 'PUT':
        # NOTE: username can not be changed because of the way the database is set up
        user_info = request.get_json()
        id = user_info['id']
        firstName = user_info['firstName']
        lastName = user_info['lastName']
        email = user_info['email']
        password = user_info['password']
        phone = user_info['phone']
        userStatus = user_info['userStatus']
        if id < 0:
            abort(400)

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

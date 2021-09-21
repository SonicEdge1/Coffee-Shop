# Link to get JWT token
# https://joes-coffee-shop.us.auth0.com/authorize?audience=CoffeeShopAPI&response_type=token&client_id=fjb33CnyG41x67vtWHdhTREa450KpVkh&redirect_uri=http://localhost:8080/login-results


import json
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

OK = 200
BAD_REQUEST = 400
BAD_REQUEST_MSG = "Bad Request"
UNAUTHORIZED = 401
UNAUTHORIZED_MSG = "Unauthorized"
FORBIDDEN = 403
FORBIDDEN_MSG = "Forbidden"
RESOURCE_NOT_FOUND = 404
RESOURCE_NOT_FOUND_MSG = "Resource Not Found"
UNPROCESSABLE_ENTITY = 422
UNPROCESSABLE_ENTITY_MSG = "Unprocessable Entity"
INTERNAL_SERVER_ERROR = 500
INTERNAL_SERVER_ERROR_MSG = "Unknown Authorization Error"

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
*** uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    '''
        GET /drinks
            public endpoint
            contains only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    try:
        all_drinks = Drink.query.all()
        drinks = [drink.short() for drink in all_drinks]
        return jsonify({
            'success': True,
            'drinks': drinks,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    '''
        GET /drinks-detail
            requires the 'get:drinks-detail' permission
            contains the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    try:
        all_drinks = Drink.query.all()
        drinks = [drink.long() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    '''
        POST /drinks
            creates a new row in the drinks table
            requires the 'post:drinks' permission
            contains the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_recipe = body.get("recipe")
        new_drink = Drink(
            title=new_title,
            recipe=json.dumps(new_recipe)
        )
        new_drink.insert()
        queried_drink = Drink.query.filter(
            Drink.title == new_title).one_or_none()
        drink = [queried_drink.long()]
        return jsonify({
            'success': True,
            'drinks': drink,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    '''
        PATCH /drinks/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            updates the corresponding row for <id>
            requires the 'patch:drinks' permission
            contains the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    queried_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if queried_drink is None:
        print("drink: ", queried_drink)
        abort(RESOURCE_NOT_FOUND)
    try:
        body = request.get_json()
        edited_title = body.get("title")
        edited_recipe = body.get("recipe")
        queried_drink.title = edited_title
        queried_drink.recipe = json.dumps(edited_recipe)
        queried_drink.update()
        drink = [queried_drink.long()]
        return jsonify({
            'success': True,
            'drinks': drink,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    '''
        DELETE /drinks/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            deletes the corresponding row for <id>
            requires the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    drink = Drink.query.get(drink_id)
    if drink is None:
        print("drink: ", drink)
        abort(RESOURCE_NOT_FOUND)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": UNPROCESSABLE_ENTITY,
        "message": UNPROCESSABLE_ENTITY_MSG
    }), UNPROCESSABLE_ENTITY


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": RESOURCE_NOT_FOUND,
        "message": RESOURCE_NOT_FOUND_MSG
    }), RESOURCE_NOT_FOUND


@app.errorhandler(AuthError)
def auth_error(error):
    # 401
    if error.status_code == UNAUTHORIZED:
        return jsonify({
            "success": False,
            "error": UNAUTHORIZED,
            "message": UNAUTHORIZED_MSG
        }), UNAUTHORIZED
    # 403
    elif error.status_code == FORBIDDEN:
        return jsonify({
            "success": False,
            "error": FORBIDDEN,
            "message": FORBIDDEN_MSG
        }), FORBIDDEN
    # 400
    elif error.status_code == BAD_REQUEST:
        return jsonify({
            "success": False,
            "error": BAD_REQUEST,
            "message": BAD_REQUEST_MSG
        }), BAD_REQUEST
    else:
        return jsonify({
            "success": False,
            "error": INTERNAL_SERVER_ERROR,
            "message": INTERNAL_SERVER_ERROR_MSG
        }), INTERNAL_SERVER_ERROR

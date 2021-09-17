import os
from flask import Flask, request, abort, jsonify
from flask import abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

OK = 200
BAD_REQUEST = 400
BAD_REQUEST_MSG = "Bad Request"
RESOURCE_NOT_FOUND = 404
RESOURCE_NOT_FOUND_MSG = "Resource Not Found"
METHOD_NOT_ALLOWED = 405
METHOD_NOT_ALLOWED_MSG = "Method Not Allowed"
UNPROCESSABLE_ENTITY_MSG = "Unprocessable Entity"

app = Flask(__name__)
setup_db(app)
CORS(app)

UNPROCESSABLE_ENTITY = 422
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('get:drinks')
def get_drinks(payload):
    print(payload)
    try:
        all_drinks = Drink.query.all()
        drinks=[drink.short() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)


    '''
    test using:
    curl http://127.0.0.1:5000/questions
    reference QuestionView.js : 26
    '''

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    print(payload)
    try:
        all_drinks = Drink.query.all()
        drinks=[drink.long() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks,
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    print(payload)
    try:
        #TODO //fix this to grab info from the webpage
        # body = request.get_json()
        # new_title = body.get('title')
        # new_recipe = body.get('recipe')
        #TODO //if the title is the same as one in the DB, then the insert will fail  Catch it?
        # new_drink=Drink(
        #     title=new_title,
        #     recipe=new_recipe
        # )
        new_drink=Drink(
            title='3 Chocolate',
            recipe='[{"name": "water", "color": "blue", "parts": 1}, {"name": "Hot Chocolate Mix", "color": "brown", "parts": 3}]'
        )
        new_drink.insert()
        print("new_drink", new_drink)
        # all_drinks = Drink.query.all()
        # drinks=[drink.long() for drink in all_drinks]
        # drinks=[drink.long() for drink in new_drink]


        return jsonify({
            'success': True,
            'drinks': new_drink.long(),
        }), OK
    except Exception as e:
        print("Exception: ", e)
        abort(UNPROCESSABLE_ENTITY) 

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

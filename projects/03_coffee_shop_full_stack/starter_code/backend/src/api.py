import os
import sys
from flask import Flask, request, jsonify, abort
from flask_httpauth import HTTPTokenAuth
from functools import wraps
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

auth = HTTPTokenAuth(scheme='Bearer')
app = Flask(__name__)
setup_db(app)
CORS(app)

@app.route('/drinks')
def get_drinks():
    data = Drink.query.all()
    drinks = [drink.short() for drink in data]
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    try:
        data = Drink.query.all()
        drinks = []
        if data:
            drinks = [drink.long() for drink in data]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():
    try:
        data = request.get_json()
        new_drink = Drink(
            title=data.get('title'),
            recipe=json.dumps(
                data.get('recipe')))
        new_drink.insert()
        drinks = [new_drink.long()]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(id):
    data = request.get_json()
    drink = Drink.query.get(id)
    if drink is None:
        return json.dumps({
            'success':
            False,
            'error':
            'Drink #' + id + ' not found to be edited'
        }), 404
    try:
        if data.get('title'):
            drink.title = data.get('title')
        if data.get('recipe'):
            drink.recipe = data.get('recipe')
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return json.dumps({
            'success':
            False,
            'error':
            'Drink #' + id + ' not found to be deleted'
        }), 404
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)


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


@app.errorhandler(404)
def error_404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def error_401(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Unauthorized"
    }), error


@app.errorhandler(403)
def error_403(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Forbidden"
    }), error


@app.errorhandler(AuthError)
def authError(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error.get('description')

    }), error.status_code

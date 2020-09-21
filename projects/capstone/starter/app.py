import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  return app

APP = create_app()

@APP.route('/actors')
def get_actors():
  try:
    actors = Actor.query.all()
    actors = list(map(lambda e: e.json(), actors))
    return jsonify({
      'success': True,
      'actors': actors
    }), 200
  except:
    print(sys.exc_info())
    abort(422)

@APP.route('/movies')
def get_movies():
  try:
    movies = Movie.query.all()
    movies = list(map(lambda e: e.json(), movies))
    return jsonify({
      'success': True,
      'movies': movies
    }), 200
  except:
    print(sys.exc_info())
    abort(422)

###################### POST routes

@APP.route('/actors', methods=['POST'])
def create_actor():
  try:
    data = request.get_json()
    actor = Actor(data.get('name'), data.get('age'), data.get('gender'))
    actor.create()
    return jsonify({
      'success': True,
      'created': actor.id
    }), 201
  except:
    print(sys.exc_info())
    abort(422)

@APP.route('/movies', methods=['POST'])
def create_movie():
  try:
    data = request.get_json()
    movie = Movie(data.get('title'), data.get('release_date'))
    movie.create()
    return jsonify({
      'success': True,
      'created': movie.id
    }), 201
  except:
    print(sys.exc_info())
    abort(422)

###################### PATCH routes

@APP.route('/actors', methods=['PATCH'])
def patch_actor():
  try:
    data = request.get_json()
    id = data.get('id', None)
    if id is None:
      abort(400)
    actor = Actor.query.get(id)
    if data.get('name'):
      actor.name = data.get('name')
    if data.get('age'):
      actor.age = data.get('age')
    if data.get('gender'):
      actor.gender = data.get('gender')
    actor.patch()
    return jsonify({
      'success': True,
      'patched': actor.json()
    }), 200
  except:
    print(sys.exc_info())
    abort(422)

@APP.route('/movies', methods=['PATCH'])
def patch_movie():
  try:
    data = request.get_json()
    id = data.get('id', None)
    if id is None:
      abort(400)
    movie = Movie.query.get(id)
    if data.get('title'):
      movie.title = data.get('title')
    if data.get('release_date'):
      movie.release_date  = data.get('release_date')
    movie.patch()
    return jsonify({
      'success': True,
      'movie': movie.json()
    }), 200
  except:
    print(sys.exc_info())
    abort(422)

###################### DELETE routes

@APP.route('/actors/<int:id>', methods=['DELETE']) 
def delete_actor(id):
  try:
    actor = Actor.query.get(id)
    print(actor)
    actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor.json()
    })
  except:
    print(sys.exc_info())
    abort(422);

@APP.route('/movies/<int:id>', methods=['DELETE']) 
def delete_movie(id):
  try:
    movie = Movie.query.get(id)
    if movie is None:
      abort(404)
    print(movie)
    movie.delete()
    return jsonify({
      'success': True,
      'deleted': movie.json()
    })
  except:
    print(sys.exc_info())
    abort(422)


###################### Error handlers

@APP.errorhandler(400)
def error_400(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Error in request format"
    }), 400

@APP.errorhandler(401)
def error_401(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Unauthorized"
    }), error


@APP.errorhandler(403)
def error_403(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Forbidden"
    }), error


@APP.errorhandler(404)
def error_404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

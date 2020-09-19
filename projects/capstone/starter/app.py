import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

APP = create_app()

@APP.route('/actors')
def get_actors():
  try:
    actors = Actor.query.all()
    return jsonify({
      'success': True,
      'actors': actors
    }), 200
  except:
    print(sys.exc_info())
    abort(403)

@APP.route('/movies')
def get_movies():
  try:
    movies = Movie.query.all()
    return jsonify({
      'success': True,
      'movies': movies
    }), 200
  except:
    print(sys.exc_info())
    abort(403)

###################### POST routes

@APP.route('/actors', methods=['POST'])
def create_actor():
  try:
    data = request.get_json()
    actor = Actor(name=data.get('name'), age=data.get('age'), gender=data.get('gender'))
    actor.create()
  except:
    print(sys.exc_info())
    abort(403)

@APP.route('/movies', methods=['POST'])
def create_movie():
  try:
    data = request.get_json()
    movie = Movie(title=data.get('title'), release_date=data.get('release_date'))
    movie.create()
  except:
    print(sys.exc_info())
    abort(403)


###################### DELETE routes

@APP.route('/actors/<int:id>', methods=['DELETE']) 
def delete_actor(id):
  try:
    actor = Actor.get(id)
    print(actor)
    actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor.id
    })
  except:
    print(sys.exc_info())
    abort(403);

@APP.route('/movies/<int:id>', methods=['DELETE']) 
def delete_movie(id):
  try:
    movie = Movie.get(id)
    if movie is None:
      abort(404)
    print(movie)
    movie.delete()
    return jsonify({
      'success': True,
      'deleted': movie.id
    })
  except:
    print(sys.exc_info())
    abort(403)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
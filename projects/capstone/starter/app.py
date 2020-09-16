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
    actors = Actor.query.all();
    return jsonify({
      'success': True,
      'actors': actors
    }), 200
  except:
    print(sys.exc_info())
    return jsonify({
      'success': False
    }), 403

@APP.route('/movies')
def get_movies():
  try:
    movies = Movie.query.all();
    return jsonify({
      'success': True,
      'movies': movies
    }), 200
  except:
    print(sys.exc_info())
    return jsonify({
      'success': False
    }), 403

@APP.route('/actors', methods=['DELETE']) 
def delete_actor():
  return jsonify({
    'success': True
  }), 200

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
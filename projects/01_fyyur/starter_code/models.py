from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from datetime import datetime
app = Flask('app')
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue')

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'

    def get_shows(self):
      shows_query = Show.query.filter(Show.venue_id == self.id)
      upcoming_shows  = shows_query.filter(Show.start_time > datetime.now()).all()
      past_shows      = shows_query.filter(Show.start_time <= datetime.now()).all()
      self.upcoming_shows_count = len(upcoming_shows)
      self.upcoming_shows = upcoming_shows
      self.past_shows_count = len(past_shows)
      self.past_shows = past_shows

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist')

    def __repr__(self):
      return f'<Artist {self.id} {self.name}>'

    def get_shows(self):
      shows_query = Show.query.filter(Show.artist_id == self.id)
      upcoming_shows  = shows_query.filter(Show.start_time > datetime.now()).all()
      past_shows      = shows_query.filter(Show.start_time <= datetime.now()).all()
      self.upcoming_shows_count = len(upcoming_shows)
      self.upcoming_shows = upcoming_shows
      self.past_shows_count = len(past_shows)
      self.past_shows = past_shows

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show {self.id} {self.artist_id} {self.venue_id} {self.start_time}>'

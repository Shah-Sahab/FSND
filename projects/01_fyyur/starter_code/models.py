from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from flask import Flask

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
    # "website": "https://www.themusicalhop.com",
    # "facebook_link": "https://www.facebook.com/TheMusicalHop",
    # "seeking_talent": True,
    # "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    # "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return (
          f"""<Venue ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone},' 
          'genres: {self.genres}, website: {self.website}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, seeking_talent: {self.seeking_talent}'
          'seeking_description: {self.seeking_description}, shows: {self.shows}""")
    # artists = db.relationship('Artist', secondary=show, back_ref=db.backref('venues', lazy=True))
    # products = db.relationship('Product', secondary=order_items,
    #   backref=db.backref('orders', lazy=True))

    def serialize(self):
      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'address': self.address,
        'genres': self.genres,
        'website': self.website,
        'phone': self.phone,
        'image_link': self.image_link,
        'facebook_link': self.facebook_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description,
        'past_shows': self.past_shows,
        'upcoming_shows': self.future_shows,
        'past_shows_count': self.past_shows_count,
        'upcoming_shows_count': self.future_shows_count
      }

    @property
    def past_shows(self):
      now = datetime.now()
      # '%Y-%m-%dT%H:%M:%S.%fZ'
      past_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return past_shows

    @property
    def past_shows_count(self):
      return len(self.past_shows)

    @property
    def future_shows(self):
      now = datetime.now()
      # '%Y-%m-%dT%H:%M:%S.%fZ'
      future_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > now]
      return future_shows

    @property
    def future_shows_count(self):
      return len(self.future_shows)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return (
          f"""<Venue ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone},' 
          'genres: {self.genres}, website: {self.website}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, seeking_venue: {self.seeking_venue}'
          'seeking_description: {self.seeking_description}, shows: {self.shows}""")

    def serialize(self):
      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'genres': self.genres,
        'website': self.website,
        'image_link': self.image_link,
        'facebook_link': self.facebook_link,
        'seeking_venue': self.seeking_venue,
        'seeking_description': self.seeking_description,
        'past_shows': self.past_shows,
        'upcoming_shows': self.future_shows,
        'past_shows_count': self.past_shows_count,
        'upcoming_shows_count': self.future_shows_count
      }
    
    @property
    def past_shows(self):
      now = datetime.now()
      # '%Y-%m-%dT%H:%M:%S.%fZ'
      past_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return past_shows

    @property
    def past_shows_count(self):
      return len(self.past_shows)

    @property
    def future_shows(self):
      now = datetime.now()
      future_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > now]
      return future_shows

    @property
    def future_shows_count(self):
      return len(self.future_shows)

class Show(db.Model):
  __tablename__ = 'Show'
  # __table_args__ = (
  #   PrimaryKeyConstraint('venue_id', 'artist_id')
  # )
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.String(), nullable=False)

  def serialize(self):
    return {
      'venue_id': self.venue_id,
      'artist_id': self.artist_id,
      'start_time': self.start_time
    }


# show = db.Table('show',
# db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
# db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
# db.Column('start_time', db.DateTime)
# )

#!/usr/bin/python3
""" Models for database tables """
import pymysql
from flask_sqlalchemy import SQLAlchemy
from soundhood import app


db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:root@localhost/soundhood'
)
db.init_app(app)



user_liked_album = db.Table(
        'user_liked_album',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

user_liked_track = db.Table(
    'user_liked_track',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True)
)

user_top_track = db.Table(
    'user_top_track',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True)
)

user_liked_playlist = db.Table(
    'user_liked_playlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)


class Album(db.Model):
    """Album table model."""
    id = db.Column(db.Integer, primary_key=True)
    spotify_album_id = db.Column(db.String(30), unique=True, nullable=False)
    album_name = db.Column(db.String(100), nullable=False)
    album_cover_image = db.Column(db.LargeBinary)
    album_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Return a string representation of the Album."""
        return f'Album(id={self.id}, spotify_album_id={self.spotify_album_id}, album_name={self.album_name}, ' \
               f'album_cover_image={self.album_cover_image}, album_url={self.album_url})'

    def __str__(self):
        """Return a string representation of the Album."""
        return f'Album: {self.album_name} ({self.album_url})'


class Track(db.Model):
    """Track table model."""
    id = db.Column(db.Integer, primary_key=True)
    spotify_track_id = db.Column(db.String(30), unique=True, nullable=False)
    track_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Return a string representation of the Track."""
        return f'Track(id={self.id}, spotify_track_id={self.spotify_track_id}, track_url={self.track_url})'

    def __str__(self):
        """Return a string representation of the Track."""
        return f'Track: {self.spotify_track_id}'


class Playlist(db.Model):
    """Playlist table model."""
    id = db.Column(db.Integer, primary_key=True)
    spotify_playlist_id = db.Column(db.String(30), unique=True, nullable=False)
    owner_id = db.Column(db.String(30), nullable=False)
    playlist_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Return a string representation of the Playlist."""
        return f'Playlist(id={self.id}, spotify_playlist_id={self.spotify_playlist_id}, owner_id={self.owner_id}, ' \
               f'playlist_url={self.playlist_url})'

    def __str__(self):
        """Return a string representation of the Playlist."""
        return f'Playlist: {self.spotify_playlist_id}'



class User(db.Model):
    """User table model."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    spotify_user_id = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(10))
    user_name = db.Column(db.String(20))
    main_photo = db.Column(db.LargeBinary)
    birthday = db.Column(db.Date)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    country = db.Column(db.String(60))
    albums = db.relationship('Album', secondary=user_liked_album, backref=db.backref('users_album', lazy='dynamic'))
    tracks = db.relationship('Track', secondary=user_liked_track, backref=db.backref('users_tracks', lazy='dynamic'))
    playlists = db.relationship('Playlist', secondary=user_liked_playlist, backref=db.backref('users_playlist', lazy='dynamic'))
    toptracks = db.relationship('Track', secondary=user_top_track, backref=db.backref('users_top', lazy='dynamic'))

    def __repr__(self):
        """Return a string representation of the User."""
        return f'User(id={self.id}, email={self.email}, spotify_user_id={self.spotify_user_id}, ' \
               f'password={self.password}, user_name={self.user_name}, main_photo={self.main_photo}, ' \
               f'birthday={self.birthday}, created_at={self.created_at}, modified_at={self.modified_at}, ' \
               f'country={self.country})'

    def __str__(self):
        """Return a string representation of the User."""
        return f'User: {self.user_name} ({self.email})'


with app.app_context():
    db.create_all()

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    drives = db.relationship('Drive', backref='game', lazy=True, cascade="all, delete-orphan")

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    result = db.Column(db.String(50))
    plays = db.relationship('Play', backref='drive', lazy=True, cascade="all, delete-orphan")

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    quarter = db.Column(db.Integer)
    down = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    yard_line = db.Column(db.Integer)
    play_type = db.Column(db.String(50))
    play_direction = db.Column(db.String(20))  # Added this field
    result = db.Column(db.String(50))
    gain_loss = db.Column(db.Integer)
    personnel = db.Column(db.String(20))
    off_form = db.Column(db.String(50))
    form_adj = db.Column(db.String(50))
    dir_call = db.Column(db.String(50))
    off_play = db.Column(db.String(50))
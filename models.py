from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    total_runs = db.Column(db.Integer, default=0)
    total_wickets = db.Column(db.Integer, default=0)
    total_overs = db.Column(db.Integer, default=0)

class Over(db.Model):
    __tablename__ = 'overs'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    ball_number = db.Column(db.Integer, nullable=False)
    runs_scored = db.Column(db.Integer, nullable=False)
    is_wicket = db.Column(db.Boolean, default=False)

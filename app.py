from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/crickscore_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    total_runs = db.Column(db.Integer, default=0)
    total_wickets = db.Column(db.Integer, default=0)
    total_overs = db.Column(db.Integer, default=0)

class Over(db.Model):
    over_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.match_id'))
    ball_number = db.Column(db.Integer)
    runs_scored = db.Column(db.Integer)
    is_wicket = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    runs = data['runs']
    is_wicket = data['is_wicket']
    # Update the database with the new score
    match = Match.query.first()  # Assuming there is only one match for simplicity
    match.total_runs += runs
    db.session.commit()

    # Emit to the user view about the score update
    socketio.emit('score_update', {'runs': match.total_runs, 'wickets': match.total_wickets})
    return jsonify({'status': 'success', 'runs': match.total_runs})

@socketio.on('connect')
def handle_connect():
    print('User connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)

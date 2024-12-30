from flask_socketio import SocketIO, emit
from app import socketio
from models import db, RealTimeUpdate

@socketio.on('connect')
def handle_connect():
    print("User connected.")

@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected.")

@socketio.on('score_update')
def handle_score_update(data):
    match_id = data['match_id']
    event_data = f"Score updated: {data['runs']} runs on ball {data['ball_number']}"
    
    update = RealTimeUpdate(match_id=match_id, event_type="score_update", event_data=event_data)
    db.session.add(update)
    db.session.commit()

    emit('score_update', {'message': event_data}, broadcast=True)

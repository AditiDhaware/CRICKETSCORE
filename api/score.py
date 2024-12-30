from flask import Blueprint, request, jsonify
from models import db, Match, Over
from flask_socketio import SocketIO, emit

score_bp = Blueprint('score', __name__)

# Get current match score
@score_bp.route('/current_score', methods=['GET'])
def get_current_score():
    match = Match.query.first()
    return jsonify({
        'total_runs': match.total_runs,
        'total_wickets': match.total_wickets,
        'total_overs': match.total_overs
    })

# Update score for the current ball
@score_bp.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    match = Match.query.first()
    over = Over.query.filter_by(match_id=match.match_id).order_by(Over.ball_number.desc()).first()
    
    new_over = Over(
        match_id=match.match_id,
        ball_number=over.ball_number + 1,
        runs_scored=data['runs'],
        is_wicket=data['is_wicket']
    )
    
    db.session.add(new_over)
    match.total_runs += data['runs']
    if data['is_wicket']:
        match.total_wickets += 1
    match.total_overs += 1 if new_over.ball_number == 6 else 0
    db.session.commit()

    emit('score_update', {'match_id': match.match_id, 'runs': data['runs'], 'ball_number': new_over.ball_number}, broadcast=True)
    
    return jsonify({"message": "Score updated successfully."})

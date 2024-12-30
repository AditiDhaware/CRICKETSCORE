from flask import Blueprint, request, jsonify
from models import db, Match, Over

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/current_score', methods=['GET'])
def get_current_score():
    match = Match.query.first()
    if match:
        return jsonify({
            "total_runs": match.total_runs,
            "total_wickets": match.total_wickets,
            "total_overs": match.total_overs
        })
    return jsonify({"total_runs": 0, "total_wickets": 0, "total_overs": 0})

@api_blueprint.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    match = Match.query.first()
    if not match:
        match = Match()
        db.session.add(match)
        db.session.commit()

    over = Over.query.filter_by(match_id=match.id).order_by(Over.id.desc()).first()
    ball_number = over.ball_number + 1 if over else 1
    is_wicket = data.get('is_wicket', False)
    runs_scored = data.get('runs_scored', 0)

    new_ball = Over(match_id=match.id, ball_number=ball_number, runs_scored=runs_scored, is_wicket=is_wicket)
    db.session.add(new_ball)

    # Update match totals
    match.total_runs += runs_scored
    if is_wicket:
        match.total_wickets += 1
    db.session.commit()

    return jsonify({"message": "Score updated successfully!"})

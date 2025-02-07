from flask import Blueprint, jsonify, render_template
from flask import request
from app.models.responses import Response
from app.models.questions import Question
from app.models.questions import Statistic
from app.schemas.questions import MessageAddResponse
from app.models import db
import pandas as pd

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')



@responses_bp.route('/', methods=['GET'])
def get_statistic():
    statistics = Statistic.query.all()
    resp_data = [{
        'question_id': db.session.query(Question.text).filter(Question.id==statistic.question_id).first(),
        'agree': statistic.agree_count,
        'disagree': statistic.disagree_count,

    } for statistic in statistics]
    # return jsonify(resp_data)
    return pd.DataFrame(resp_data).to_html()


@responses_bp.route('/', methods=['POST'])
def add_response():
    data = request.get_json()
    cool_data = MessageAddResponse(**data)
    question = Question.query.get(cool_data.question_id)
    if not question:
        return jsonify({'message': 'No question provided'}), 400

    stat = Statistic.query.get(cool_data.question_id)

    if not stat:
        stat = Statistic(
            question_id=question.id,
            agree_count=0,
            disagree_count=0
        )
        db.session.add(stat)

    if cool_data.answer:
        stat.agree_count += 1
    else:
        stat.disagree_count += 1

    db.session.commit()


    return jsonify({'message': f'Successfully added a response to question {question.id}'}), 201






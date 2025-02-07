from flask import Blueprint, jsonify, request
from app.models.questions import Question, category_id_by_name, Category
import pandas as pd
from app.models import db
from app.schemas.questions import CreateQuestion, ResponseQuestion


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')



@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    questions_data = [ResponseQuestion.model_validate(q).model_dump() for q in questions]
    cat_names = []
    for q in questions_data:
        print(q)
        q_info = {
            'text': q['text'],
            'category': Category.query.filter(Category.id == q['category_id']).first().name,
        }
        cat_names.append(q_info)
    return jsonify(cat_names)




@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()
    try:
        category_id = category_id_by_name(data)
        if category_id is None or 'text' not in data:
            return jsonify({'message': 'Invalid category or text provided'}), 400
        question_data = CreateQuestion(text=data['text'], category_id=category_id)
        question = Question(text=question_data.text, category_id=question_data.category_id)
        db.session.add(question)
        db.session.commit()
        return jsonify({'message': 'Question created successfully'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    category_id = question.category_id
    if question is None or category_id is None:
        return jsonify({'message': 'Question not found'}), 404
    return jsonify({'message': f'Question found: {question.text}, category: {Category.query.get(question.category_id).name}'}), 200


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Question not found'}), 404
    data = request.get_json()
    category_id = Category.query.filter(Category.name == data['category']).first().id
    if category_id:
        data['category_id'] = category_id
        cool_data = ResponseQuestion(**data)
        question.text = cool_data.text
        category_id = category_id_by_name(data)
        question.category_id = category_id
        db.session.commit()
        return jsonify({'message': f'Question with id {question.id} was update: {question.text}'}), 200
    return jsonify({'message': 'Category not found'}), 404

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Question not found'}), 404
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f'Answer with id: {question.id} deleted'}), 200


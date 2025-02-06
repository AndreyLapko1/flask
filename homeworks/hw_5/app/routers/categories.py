from flask import Blueprint, jsonify, request
from app.models.questions import Question, Category
import pandas as pd
from app.models import db
from app.schemas.questions import CreateQuestion, ResponseQuestion, MessageResponse


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')




@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify({'message': 'No categories found'})
    q = [category.name for category in categories]
    return pd.DataFrame(q).to_html()



@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'message': 'Category not found'}), 404
    return jsonify({'message': f'Category found: {category.name}'}), 200



@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    if data is None or "name" not in data:
        return jsonify({"message": "missing name"}), 400
    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": f'category {data["name"]} was added'} ), 201


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"message": "missing data"}), 400
    category.name = data["name"]
    db.session.commit()
    return jsonify({"message": f'Category {data["name"]} was updated'}), 200

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f'Category {category_id} was deleted'}), 200


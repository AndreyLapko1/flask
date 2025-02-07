from app.models import db



class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    text = db.Column(db.Text, nullable=False)
    responses = db.relationship("Response", backref="question", lazy='joined')

    def __repr__(self):
        return f'<Question id={self.id}, text={self.text}, category={self.category_id}>'


class Statistic(db.Model):
    __tablename__ = 'statistic'
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)



class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def category_id_by_name(data: dict) -> int | None:
    category_name = data.get('category')
    if category_name is None:
        return None
    category = Category.query.filter(Category.name == category_name).first()
    if category is None:
        return None
    return category.id

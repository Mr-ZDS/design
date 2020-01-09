from datetime import datetime

from note.extensions import db


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answer_name = db.relationship('Users', backref=db.backref('answers'))
    question = db.relationship('Question', backref=db.backref('answers',
                                                              order_by=id.desc()))

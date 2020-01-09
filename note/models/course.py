from datetime import datetime

from note.extensions import db


# 一级目录模型
class Course1(db.Model):
    __tablename__ = 'course1'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10))  # 笔记状态，是否公开
    create_time = db.Column(db.DateTime, default=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('class'))


# 二级目录模型
class Course2(db.Model):
    __tablename__ = 'course2'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10))  # 笔记状态，是否公开
    create_time = db.Column(db.DateTime, default=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('class1'))
    course1_id = db.Column(db.Integer, db.ForeignKey('course1.id'))
    course1 = db.relationship('Course1', backref=db.backref('class1'))

    __mapper_args__ = {"order_by": create_time.desc()}


# 上传文件模型
class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    intro = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'))
    status = db.Column(db.String(10))  # 文件状态，是否公开
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', backref=db.backref('users'))
    course1_id = db.Column(db.Integer, db.ForeignKey('course1.id'))
    course1 = db.relationship('Course1', backref=db.backref('course1'))

    __mapper_args__ = {"order_by": create_time.desc()}

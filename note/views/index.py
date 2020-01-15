from flask import Blueprint, render_template, request
from sqlalchemy import desc

from note.models.communicate import Question, Answer
from note.models.course import Course2, Upload

index_router = Blueprint("index", __name__)


@index_router.route("/")
def index():
    return render_template('index/index.html')


# 交流区、可公开的笔记、可公开的文件展示
@index_router.route('/all_home/')
def all_home():
    context = {
        "course2": Course2.query.filter(Course2.status == '公开').all(),
        "questions": Question.query.order_by(desc('create_time')).all(),
        "upload": Upload.query.filter(Upload.status == '公开').all()
    }
    return render_template('index/all_home.html', **context)


@index_router.route('/search/')
def search():
    search_content = request.args.get('search')
    context = {
        "course2": Course2.query.filter(Course2.status == '公开',
                                        Course2.title.contains(
                                            search_content)).all(),
        "questions": Question.query.filter(
            Question.title.contains(search_content)).order_by(
            desc('create_time')).all(),
        "upload": Upload.query.filter(Upload.status == '公开',
                                      Upload.file_name.contains(
                                          search_content)).all()
    }
    return render_template('index/all_home.html', **context)


# 按评论数显示可公开文本、文件
@index_router.route('/rep_sort_home/')
def rep_sort_home():
    questions = Question.query.all()
    visit = []
    for question in questions:
        count = Answer.query.filter(Answer.question_id == question.id).count()
        visit.append([question, count])
    # 评论数倒序
    res = sorted(visit, key=(lambda x: x[1]), reverse=True)

    return render_template('index/rep_sort_home.html', res=res)

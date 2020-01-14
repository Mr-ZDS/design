from flask import Blueprint, render_template, request, flash, redirect, session, \
    url_for
from flask_login import login_required
from sqlalchemy import desc

from note.extensions import db
from note.forms.communicate import CommForm, RecommForm
from note.models.communicate import Question, Answer
from note.models.user import Users

communicate_router = Blueprint("communicate", __name__)


# 交流区代码,首页
@communicate_router.route('/communicate_home/')
def communicate_home():
    context = {'questions': Question.query.order_by(desc('create_time')).all()}
    return render_template('communicate/communicate_home.html', **context)


# 交流区发言
@communicate_router.route('/communicate_release/', methods=['GET', 'POST'])
@login_required
def communicate_release():
    comm_form = CommForm()
    if request.method == 'GET':
        return render_template('communicate/release.html', form=comm_form)
    else:
        if not comm_form.validate_on_submit():
            flash(comm_form.errors)
            return render_template('users/register.html', form=comm_form)
        question = Question(title=comm_form.title.data,
                            content=comm_form.content.data)
        user_id = session.get('user_id')
        user = Users.query.filter(Users.id == user_id).first()
        question.users = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('communicate.communicate_home'))


# 原生表单视图
# @communicate_router.route('/communicate_release/', methods=['GET', 'POST'])
# @login_required
# def communicate_release():
#     if request.method == 'GET':
#         return render_template('communicate/release.html')
#     else:
#         title = request.form.get('title')
#         content = request.form.get('content')
#         # 去除两端空格不能为空字符
#         if len(title.strip()) == 0 or len(title) > 100:
#             flash('标题不能为空或超过100个字符！！！')
#             return render_template('communicate/release.html')
#         if len(content.strip()) == 0:
#             flash('请填写您的内容！！！')
#             return render_template('communicate/release.html')
#         question = Question(title=title, content=content)
#         user_id = session.get('user_id')
#         user = Users.query.filter(Users.id == user_id).first()
#         question.users = user
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('communicate.communicate_home'))


# 发言详情
@communicate_router.route('/communicate_detail/<question_id>')
def communicate_detail(question_id):
    questions = Question.query.filter(Question.id == question_id).first()
    count = Answer.query.filter(Answer.question_id == question_id).count()
    return render_template('communicate/detail.html', question=questions,
                           count=count)


# 发言评论
@communicate_router.route('/communicate_replies/', methods=['POST'])
@login_required
def communicate_replies():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    user_id = session['user_id']
    answer = Answer(content=content)
    user = Users.query.filter(Users.id == user_id).first()
    answer.answer_name = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    if len(content.strip()) == 0:
        flash('评论不能为空！！！')
        return redirect(
            url_for('communicate.communicate_detail', question_id=question_id))
    db.session.add(answer)
    db.session.commit()
    return redirect(
        url_for('communicate.communicate_detail', question_id=question_id))


# 个人发言中心，统计
@communicate_router.route('/communicate_personal/')
@login_required
def communicate_personal():
    user_id = session['user_id']
    questions = Question.query.filter(Question.user_id == user_id).all()
    count = Question.query.filter(Question.user_id == user_id).count()
    return render_template('communicate/personal.html', questions=questions,
                           count=count)


# 删除自己的发言
@communicate_router.route('/communicate_delete/<question_id>')
def communicate_delete(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    answers = Answer.query.filter(Answer.question_id == question_id).all()
    for answer in answers:
        db.session.delete(answer)
        db.session.commit()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('communicate.communicate_personal'))


@communicate_router.route('/update_comm/<question_id>', methods=['GET', 'POST'])
def update_comm(question_id):
    form = RecommForm()
    question = Question.query.filter(Question.id == question_id).first()
    form.title.data = question.title
    form.content.data = question.content
    if request.method == 'GET':
        return render_template('communicate/update_comm.html', form=form)
    else:
        if not form.validate_on_submit():
            flash(form.errors)
            return render_template(
                'communicate/update_comm.html',
                form=form
            )
        form1 = RecommForm()
        question.title = form1.title.data
        question.content = form1.content.data
        db.session.commit()
        return redirect(url_for('communicate.communicate_home'))

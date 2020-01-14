import os

from flask import Blueprint, render_template, request, flash, redirect, session, \
    url_for
from flask_login import login_user, logout_user
from werkzeug.utils import secure_filename

from note.extensions import db
from note.forms.user import LoginForm, RegisterForm, ReiconForm
from note.models.user import Users
from note.util.decorators import delete_icon

user_router = Blueprint("user", __name__)


# 注册,wtform表单
@user_router.route("/register/", methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    login_form = LoginForm()
    if request.method == "GET":
        return render_template(
            'users/register.html',
            form=reg_form
        )
    else:
        if not reg_form.validate_on_submit():
            flash(reg_form.errors)
            return render_template('users/register.html', form=reg_form)

        if Users.query.filter(Users.username == reg_form.username.data).first():
            flash('该用户名已被使用，请重新输入！！！')
            return render_template('users/register.html', form=reg_form)
        user = Users.query.filter(
            Users.telephone == reg_form.telephone.data).first()
        if user:
            flash('该手机号码已注册，请登录或重新注册！！！')
            return render_template('users/register.html', form=reg_form)
        users = Users(telephone=reg_form.telephone.data,
                      username=reg_form.username.data,
                      password=reg_form.password.data)
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('user.login', form=login_form))


# 原生表单
# @user_router.route("/register/", methods=['GET', 'POST'])
# def register():
#     if request.method == "GET":
#         return render_template('users/register.html')
#     else:
#         telephone = request.form.get('telephone')
#         username = request.form.get('username')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#
#         if Users.query.filter(Users.username == username).first():
#             flash('该用户名已被使用，请重新输入！！！')
#             return render_template('users/register.html')
#         if len(telephone) != 11:
#             flash('手机号码格式错误！！！')
#             print(telephone)
#             return render_template('users/register.html')
#         else:
#             user = Users.query.filter(Users.telephone == telephone).first()
#             if user:
#                 flash('该手机号码已注册，请登录或重新注册！！！')
#                 return render_template('users/register.html')
#             if len(password1) < 5 or len(password1) > 20:
#                 flash('密码长度为5-20个字符！！！')
#                 return render_template('users/register.html')
#             if password1 != password2:
#                 flash('两次密码不相同！请重新输入!!!')
#                 return render_template('users/register.html')
#             else:
#                 users = Users(telephone=telephone, username=username,
#                               password=password1)
#                 db.session.add(users)
#                 db.session.commit()
#                 return redirect(url_for('user.login'))


# 登录，wtf表单
@user_router.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('users/login.html', form=form)
    else:
        if not form.validate_on_submit():
            flash(form.errors)
            return render_template('users/login.html', form=form)
        users = Users.query.filter(
            Users.telephone == form.telephone.data).first()
        login_user(users)
        if users and users.check_password(form.password.data):
            session['user_id'] = users.id
            session.permanent = True
            return redirect(url_for('index.index'))
        else:
            flash('账号或密码错误！！！')
            return render_template(
                'users/login.html',
                form=form
            )


# 原生登录表单
# @user_router.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('users/login.html')
#     else:
#         telephone = request.form.get('telephone')
#         password = request.form.get('password')
#         users = Users.query.filter(Users.telephone == telephone).first()
#         login_user(users)
#         if users and users.check_password(password):
#             session['user_id'] = users.id
#             session.permanent = True
#             return redirect(url_for('index.index'))
#         else:
#             flash('账号或密码错误！！！')
#             return render_template('users/login.html')


# 图片上传限制格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS


# 注销
@user_router.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user_router.route('/re_icon/', methods=['GET', 'POST'])
@delete_icon
def re_icon():
    form = ReiconForm()
    user_id = session.get('user_id')
    if request.method == 'GET':
        return render_template(
            'users/reicon.html',
            form=form
        )
    else:
        f = request.files['file']
        if allow_file(f.filename):
            # 当前文件所在路径
            basepath = os.path.dirname(__file__)
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            upload_path = os.path.join(basepath[:-6], 'static/images/icon',
                                       secure_filename(f.filename))
            f.save(upload_path)
        else:
            flash('头像格式错误或者上传错误！！！！')
            return render_template('users/reicon.html', form=form)
        if Users.query.filter(Users.icon == form.icon_name.data).first():
            flash('此头像名已存在！！！')
            return render_template('users/reicon.html', form=form)

        # 上传图像后修改数据库数据并提交
        users = Users.query.filter(Users.id == user_id).first()
        users.icon = form.icon_name.data
        db.session.commit()
        return redirect(url_for('note.home'))

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    telephone = StringField(
        validators=[
            DataRequired(message='电话号码不能为空！！！'),
            Length(11, 11)
        ],
        render_kw={
            'placeholder': '请输入手机号码',
            'class': 'form-control'
        }
    )
    password = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
        ],
        render_kw={
            'placeholder': '请输入密码',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )


class RegisterForm(FlaskForm):
    telephone = StringField(
        validators=[
            DataRequired(message='电话号码不能为空！！！'),
            Length(11, 11)
        ],
        render_kw={
            'placeholder': '请输入手机号码',
            'class': 'form-control'
        }
    )
    username = StringField(
        validators=[
            DataRequired(),
            Length(2, 10, message='用户名至少需要2个字符，最多10个字符')
        ],
        render_kw={
            'placeholder': '请输入用户',
            'class': 'form-control'
        }
    )
    password = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
            Length(5, 20)
        ],
        render_kw={
            'placeholder': '请输入密码',
            'class': 'form-control'
        }
    )
    password2 = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
            Length(5, 20),
            EqualTo('password', message="两次密码不一致!")
        ],
        render_kw={
            'placeholder': '请再次输入密码',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        '立即注册',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )

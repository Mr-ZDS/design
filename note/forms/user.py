from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


# 登录表单
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


# 注册表单
class RegisterForm(FlaskForm):
    telephone = StringField(
        validators=[
            DataRequired(message='电话号码不能为空！！！'),
            Length(11, 11, message='电话号码为11个字符')
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
            Length(5, 20, message='密码为5-20个字符')
        ],
        render_kw={
            'placeholder': '请输入密码',
            'class': 'form-control'
        }
    )
    password2 = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
            Length(5, 20, message='密码为5-20个字符'),
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


# 更换头像表单
class ReiconForm(FlaskForm):
    icon_name = StringField(
        validators=[
            DataRequired(message='请输入头像名'),
            Length(4, 20, message='头像名为4-20个字符，请正确输入')
        ],
        render_kw={
            'placeholder': '请输入头像名称',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        '立即更换',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )


# 用户资料修改表单
class UserForm(FlaskForm):
    telephone = StringField(
        validators=[
            DataRequired(message='电话号码不能为空！！！'),
            Length(11, 11, message='电话号码为11个字符')
        ],
        render_kw={
            'class': 'form-control'
        }
    )
    username = StringField(
        validators=[
            DataRequired(),
            Length(2, 10, message='用户名至少需要2个字符，最多10个字符')
        ],
        render_kw={
            'class': 'form-control'
        }
    )
    password = StringField(
        validators=[],
        render_kw={
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        '立即修改',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )


# 密码修改表单
class ResetpwordForm(FlaskForm):
    old_password = PasswordField(
        validators=[
            DataRequired(message='请输入旧密码！！！'),
        ],
        render_kw={
            'placeholder': '请输入旧密码',
            'class': 'form-control'
        }
    )
    password1 = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
            Length(5, 20, message='密码为5-20个字符')
        ],
        render_kw={
            'placeholder': '请输入新密码',
            'class': 'form-control'
        }
    )
    password2 = PasswordField(
        validators=[
            DataRequired(message='请输入密码！！！'),
            Length(5, 20, message='密码为5-20个字符'),
            EqualTo('password1', message="两次密码不一致!")
        ],
        render_kw={
            'placeholder': '请再次输入新密码',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        '立即修改',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )

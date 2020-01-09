from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommForm(FlaskForm):
    title = StringField(
        validators=[
            DataRequired(message='标题不能为空，请输入标题')
        ],
        render_kw={
            'placeholder': '请输入标题（你还可以输入100个字符）',
            'class': 'form-control'
        }
    )
    content = TextAreaField(
        validators=[
            DataRequired(message='请输入提问内容')
        ],
        render_kw={
            'placeholder': '请输入内容',
            'class': 'form-control',
            'rows': 5
        }
    )
    submit = SubmitField(
        '完成',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# 提问交流表单
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


# 评论表单
class RepForm(FlaskForm):
    answer_content = StringField(
        validators=[
            DataRequired(message='请输入评论内容')
        ],
        render_kw={
            'placeholder': '请填写你的回复',
            'class': 'form-control',
            'rows': 3
        }
    )
    submit = SubmitField(
        '立即评论',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


# 更新表单
class RecommForm(FlaskForm):
    title = StringField(
        validators=[
            DataRequired(message='标题不能为空，请输入标题')
        ],
        render_kw={
            'class': 'form-control'
        }
    )
    content = TextAreaField(
        validators=[
            DataRequired()
        ],
        render_kw={
            'class': 'form-control',
            'rows': 5
        }
    )
    submit = SubmitField(
        '立即更新',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
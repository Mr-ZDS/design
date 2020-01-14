from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length


# 一级目录表单
class Course1Form(FlaskForm):
    title = TextAreaField(
        validators=[
            DataRequired(message='标题不能为空，请输入标题'),
            Length(1, 100)
        ],
        render_kw={
            'placeholder': '请输入课程标题',
            'rows': 3,
            'cols': 70
        }
    )
    submit = SubmitField(
        '完成'
    )


# 文件上传表单
class UploadForm(FlaskForm):
    file_name = StringField(
        validators=[
            DataRequired(message='文件名不能为空！！！'),
            Length(1, 20)
        ],
        render_kw={
            'placeholder': '文件名字(包括后缀)',
            'class': 'form-control'
        }
    )
    file_intro = TextAreaField(
        validators=[
            DataRequired(message='')
        ],
        render_kw={
            'placeholder': '文件简介',
            'class': 'form-control',
            'rows': 3
        }
    )
    submit = SubmitField(
        '上传',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )


# 一级目录更新表单
class Recourse1Form(FlaskForm):
    title = TextAreaField(
        validators=[
            DataRequired(message='标题不能为空，请输入标题'),
            Length(1, 100)
        ],
        render_kw={
            'rows': 1,
            'cols': 70
        }
    )
    submit = SubmitField(
        '立即更新'
    )
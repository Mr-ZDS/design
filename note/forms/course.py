from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length


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

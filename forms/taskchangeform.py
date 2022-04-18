from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, MultipleFileField, DateField
from wtforms.validators import DataRequired


class TaskChangeForm(FlaskForm):
    # complete, files, description, deadline
    title = ""
    description = TextAreaField('описание')
    file = MultipleFileField("Файлы")
    submit = SubmitField('Сохранить')
    date = DateField('Дедлайн:')

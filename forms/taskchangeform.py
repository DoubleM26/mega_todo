from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField, MultipleFileField, DateField
from wtforms.validators import DataRequired


class TaskChangeForm(FlaskForm):
    # complete, files, description, deadline
    description = TextAreaField('описание')
    complete = BooleanField("Задача выполнена")
    file = MultipleFileField("Файлы")
    submit = SubmitField('Сохранить')
    date = DateField('Дедлайн:')

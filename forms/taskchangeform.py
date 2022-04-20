from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, MultipleFileField, DateField


class TaskChangeForm(FlaskForm):
    title = ""
    description = TextAreaField('описание')
    file = MultipleFileField("Файлы")
    submit = SubmitField('Сохранить')
    date = DateField('Дедлайн:')

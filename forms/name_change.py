from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameChangeForm(FlaskForm):
    name = StringField('Новое имя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

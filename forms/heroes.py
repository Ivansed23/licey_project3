from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class HeroesForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    clas = SelectField('Класс', choices=['Воин', 'Маг', 'Лучник', 'Жрец', 'Плут'])
    race = SelectField('Раса', choices=['Человек', 'Эльф', 'Дварф', 'Полурослик',
                                        'Гном', 'Полуэльф', 'Орк'])
    submit = SubmitField('Применить')
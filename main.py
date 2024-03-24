from flask import Flask
from flask import render_template
from data import db_session
from data.heroes import Hero
from data.races import Races
from data.classes import Classes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/characters.db")
    app.run()


if __name__ == '__main__':
    main()

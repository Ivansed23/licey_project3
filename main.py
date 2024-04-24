from flask import Flask, redirect, abort
from flask import render_template
from data import db_session
from data.heroes import Hero
from data.races import Races
from data.classes import Classes
from data.users import User
from flask import request, make_response, session
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from forms.heroes import HeroesForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/characters.db")
    app.run()


@app.route("/")
def main_page():
    return render_template('main_page.html', title='Главная страница')


@app.route("/classes")
def classes_page():
    return render_template('classes_page.html')


def search_race(query):
    db_sess = db_session.create_session()
    races = db_sess.query(Races).filter(Races.name.ilike(f'%{query}%') |
                                        Races.description.ilike(f'%{query}%')).all()
    return races


@app.route("/races")
def races_page():
    query = request.args.get('query', '').strip()
    if query:
        races = search_race(query)
    else:
        db_sess = db_session.create_session()
        races = db_sess.query(Races).all()
    return render_template('races_page.html', races=races, query=query)


@app.route("/race/<int:race_id>")
def race_details(race_id):
    db_sess = db_session.create_session()
    race = db_sess.query(Races).get(race_id)
    if not race:
        return render_template('error.html', message="Раса не найдена"), 404
    return render_template('race_details.html', race=race)


@app.route("/rules")
def rules_page():
    return render_template('rules_page.html', title='Правила')


@app.route("/my_heroes")
def my_heroes_page():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        heroes = db_sess.query(Hero).filter(Hero.user == current_user)
        return render_template("heroes_page.html", heroes=heroes)
    else:
        heroes = None
        return render_template("heroes_page.html", heroes=heroes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_hero',  methods=['GET', 'POST'])
@login_required
def add_hero():
    form = HeroesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Hero).filter(Hero.name == form.name.data).first():
            return render_template('heroes_form.html', title='Добавление персонажа',
                                   form=form, message="Герой с таким именем уже существует")
        db_sess = db_session.create_session()
        clas = db_sess.query(Classes).filter(Classes.name == form.clas.data).first()
        race = db_sess.query(Races).filter(Races.name == form.race.data).first()
        hero = Hero(name=form.name.data, class_id=clas.id, race_id=race.id)
        cur_user = db_sess.query(User).filter(User.id == current_user.id).first()
        cur_user.heroes.append(hero)
        db_sess.merge(cur_user)
        db_sess.commit()
        return redirect('/my_heroes')
    return render_template('heroes_form.html', title='Добавление персонажа',
                           form=form)


@app.route('/edit_hero/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_hero(id):
    form = HeroesForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        hero = db_sess.query(Hero).filter(Hero.id == id,
                                            Hero.user == current_user
                                            ).first()
        clas = db_sess.query(Classes).filter(Classes.id == hero.class_id).first()
        race = db_sess.query(Races).filter(Races.id == hero.race_id).first()
        if hero:
            form.name.data = hero.name
            form.clas.data = clas
            form.race.data = race
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        hero = db_sess.query(Hero).filter(Hero.id == id,
                                            Hero.user == current_user
                                            ).first()
        clas = db_sess.query(Classes).filter(Classes.name == form.clas.data).first()
        race = db_sess.query(Races).filter(Races.name == form.race.data).first()
        if db_sess.query(Hero).filter(Hero.name == form.name.data).first():
            return render_template('heroes_form.html', title='Добавление персонажа',
                                   form=form, message="Герой с таким именем уже существует")
        if hero:
            hero.name = form.name.data
            hero.class_id = clas.id
            hero.race_id = race.id
            db_sess.commit()
            return redirect('/my_heroes')
        else:
            abort(404)
    return render_template('heroes_form.html',
                           title='Редактирование героя',
                           form=form
                           )


@app.route('/delete_hero/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_hero(id):
    db_sess = db_session.create_session()
    hero = db_sess.query(Hero).filter(Hero.id == id,
                                      Hero.user == current_user
                                      ).first()
    if hero:
        db_sess.delete(hero)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/my_heroes')


if __name__ == '__main__':
    main()

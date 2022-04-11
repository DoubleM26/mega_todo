from flask import Flask, make_response, jsonify, render_template, request
from flask_restful import Api
from werkzeug.utils import redirect

from forms.login import LoginForm
from forms.name_change import NameChangeForm
from forms.add_task import AddTask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, api
from data.User import User
from data.Task import Task
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba'
# api = Api(app)
# api.add_resource(user_resources.UserListResource, "/api/users")
# api.add_resource(user_resources.UserResource, "/api/users/<int:user_id>")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/complete_tasks', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        form = AddTask()

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        tasks_data = []
        for task_id in user.tasks.split():
            task = db_sess.query(Task).filter(Task.id == int(task_id)).first()
            if request.url.split("/")[-1] and task.complete:
                tasks_data.append(task)
            elif not request.url.split("/")[-1] and not task.complete:
                tasks_data.append(task)
        tasks_data.reverse()
        if form.validate_on_submit():
            task = db_sess.query(Task).filter(Task.title == form.task_title.data).first()
            if not task:
                task = Task(title=form.task_title.data)
                db_sess.add(task)
                db_sess.commit()
                task = db_sess.query(Task).filter(Task.title == form.task_title.data).first()

                user.tasks += " " + str(task.id)
                db_sess.commit()
                return redirect("/")
            return render_template('index.html', message="Такая задача уже существует", form=form, tasks_data=tasks_data)
            # user = db_sess.query(User).filter(User.id == current_user.id).first()
        if not request.url.split("/")[-1]:
            print(request.url.split("/")[-1])
            classes = ["nav-link active", "nav-link", "nav-link"]
        else:
            classes = ["nav-link", "nav-link", "nav-link active"]
        return render_template(
            "index.html",
            title="Mega ToDo",
            form=form,
            tasks_data=tasks_data,
            classes=classes)
    return render_template("intro.html")


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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if not request.url.split("/")[-1]:
    #     classes = ["nav-link active", "nav-link", "nav-link"]
    # else:
    #     classes = ["nav-link", "nav-link", "nav-link active"]

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
    return render_template("login.html", form=form, title="Авторизация")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = NameChangeForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        print(form.name.data)
        user.name = form.name.data
        db_sess.commit()
        return redirect('/settings')
    return render_template("settings.html", title="Настройки", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/super_todo.db")
    # app.register_blueprint(api.blueprint)
    app.run(port=8080, host='127.0.0.1')

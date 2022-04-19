import os
from datetime import timedelta

from flask import Flask, make_response, jsonify, render_template, request, url_for, flash, send_file
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Api
from werkzeug.utils import redirect, secure_filename

from data.api import check_keys, create_jwt_for_user
from forms.login import LoginForm
from forms.name_change import NameChangeForm
from forms.add_task import AddTask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, api
from data.User import User
from data.Task import Task
from data.File import File
from data.api import create_jwt_for_user, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file
from forms.registerform import RegisterForm
from forms.taskchangeform import TaskChangeForm




app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba'
app.config["JWT_SECRET_KEY"] = "super-secret"  # секретный ключ для токенов
app.config["JWT_EXPIRES"] = timedelta(hours=24)  # сколько действителен jwt токен
app.config["JWT_IDENTITY_CLAIM"] = 'user'  # заголовок, где хранится информация о пользователе
app.config["JWT_HEADER_NAME"] = 'authorization'  # заголовок, куда передается токен при действиях
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)





@app.route('/')
def default():
    if not current_user.is_authenticated:
        return render_template("intro.html")
    return redirect("/todo")


@app.route('/complete_tasks/<search_data>', methods=['GET', 'POST'],
           defaults={'complete': True, 'task_id': None})
@app.route('/todo/<search_data>', methods=['GET', 'POST'],
           defaults={'complete': False, 'task_id': None})
@app.route('/task/<int:task_id>', methods=['GET', 'POST'],
           defaults={'search_data': "", 'complete': False})
@app.route('/complete_task/<int:task_id>', methods=['GET', 'POST'],
           defaults={'search_data': "", 'complete': True})
@app.route('/complete_tasks', methods=['GET', 'POST'],
           defaults={'search_data': "", 'complete': True, 'task_id': None})
@app.route('/todo', methods=['GET', 'POST'],
           defaults={'search_data': "", 'complete': False, 'task_id': None})
def main(search_data, complete, task_id):
    curr_task = None
    print(task_id, "f")
    if task_id is not None:
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.id == current_user.id).first()
        for i in user.tasks.split():
            task = db_sess.query(Task).filter(Task.id == int(i)).first()
            # print(task.id)
            if task.id == task_id:
                curr_task = task
                print(curr_task.title)

    change_task_form = TaskChangeForm()
    change_task_form.title = "Maga ToDo"
    if curr_task is not None:
        change_task_form.date.data = curr_task.deadline
        change_task_form.description.data = curr_task.description

    form = AddTask()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    tasks_data = []
    for task_id in user.tasks.split():
        task = db_sess.query(Task).filter(Task.id == int(task_id)).first()
        if search_data.lower() in task.title.lower() or search_data.lower() in task.description.lower():
            if complete and task.complete:
                tasks_data.append(task)
            elif not complete and not task.complete:
                tasks_data.append(task)
    tasks_data.reverse()
    if form.validate_on_submit():
        task = Task(title=form.task_title.data)
        db_sess.add(task)
        db_sess.commit()
        task = db_sess.query(Task).filter(Task.title == form.task_title.data)[-1]
        user.tasks += " " + str(task.id)
        db_sess.commit()
        return redirect("/")
        # user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not complete:
        classes = ["nav-link active", "nav-link", "nav-link"]
    else:
        classes = ["nav-link", "nav-link", "nav-link active"]

    #
    files = []
    if curr_task is not None:
        for i in curr_task.files.split():
            files.append(db_sess.query(File).filter(File.id == i).first())

    return render_template(
        "index.html",
        title="Mega ToDo",
        form=form,
        search_data=search_data,
        tasks_data=tasks_data,
        complete=str(complete),
        lower=lambda x: x.lower(),
        files=files,
        classes=classes, change_form=change_task_form, curr_task=curr_task)


@app.route("/first_handler/<task_name>", methods=["POST", "GET"])
@login_required
def first_handler(task_name=None):
    if task_name is None:
        return redirect("/")
    form = TaskChangeForm()

    db_sess = db_session.create_session()
    curr_task = db_sess.query(Task).filter(Task.id == task_name).first()

    curr_task.deadline = form.date.data
    curr_task.description = form.description.data

    # --

    if 'file' not in request.files:
        flash('No file part')
        db_sess.commit()
        return redirect("/")

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        db_sess.commit()
        return redirect("/")

    if file and allowed_file(file.filename):
        curr_task = db_sess.query(Task).filter(Task.id == task_name).first()
        sess_file = File()
        db_sess.add(sess_file)
        sess_file.extension = file.filename.split(".")[-1]
        db_sess.commit()
        file.filename = str(sess_file.id) + "." + sess_file.extension
        sess_file.filename = file.filename
        print("-------", str(sess_file.id))
        open(app.config['UPLOAD_FOLDER'] + "/" + str(sess_file.id) + "." + sess_file.extension,
             "wb").close()
        file.save(app.config['UPLOAD_FOLDER'] + "/" + str(sess_file.id) + "." + sess_file.extension)
        print("-----------")
        print("curr", curr_task.files)
        if curr_task.files is None:
            curr_task.files = str(sess_file.id)
        else:
            curr_task.files += " " + str(sess_file.id)
        db_sess.commit()

    if curr_task.complete:
        db_sess.commit()
        return redirect("/complete_tasks")
    db_sess.commit()
    return redirect("/")


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


@app.route('/get_file/<file_name>')
@login_required
def get_image(file_name):
    return send_file("saved_files/" + file_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            res = redirect("/")
            token = create_jwt_for_user(user)
            res.set_cookie("jwt", token.json["token"], max_age=60 * 60 * 24 * 365 * 2)
            return res

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", form=form, title="Авторизация")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = NameChangeForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        print(form.name.data)
        user.name = form.name.data
        db_sess.commit()
        return redirect('/settings')
    return render_template("settings.html", title="Настройки", form=form)


@app.route('/calendar')
def calendar():
    classes = ["nav-link", "nav-link active", "nav-link"]
    return render_template("calendar.html", title="Календарь", classes=classes)


@app.route('/test')
@login_required
def test():
    form = TaskChangeForm()
    return render_template("test.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.jwt.expired_token_loader
def my_expired_token_callback():
    err_json = {"message": "expired token"}
    return jsonify(err_json), 401


@app.jwt.invalid_token_loader
@app.jwt.unauthorized_loader
def my_inv_unauth_token_callback(why):
    err_json = {"message": why}
    return jsonify(err_json), 401


if __name__ == '__main__':
    db_session.global_init("super_todo.db")
    app.register_blueprint(api.blueprint)
    app.run(port=8080, host='127.0.0.1')

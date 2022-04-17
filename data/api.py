import flask
from flask import jsonify, request, make_response
from flask_jwt_simple import create_jwt, jwt_required
from flask_jwt_simple import get_jwt_identity
from data import db_session
from data.User import User
from data.Task import Task

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


def check_keys(dct, keys):
    return all(key in dct for key in keys)


def create_jwt_for_user(user):
    cp_user = {"name": user.name, "email": user.email}
    j_token = {'token': create_jwt(identity=cp_user)}  # создаем jwt токен
    return jsonify(j_token)


# ----получение всех пользователей----
@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'email'))
                 for item in users]
        }
    )


# ----регистрация нового пользователя----
@blueprint.route('/api/register', methods=["POST"])
def registrate_user():
    in_json = request.json
    if not in_json:
        return jsonify({"error": "Empty request"})
    elif not check_keys(in_json, ("name", 'email', 'password')):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == in_json['email']).first():
        return jsonify({"error": "Dublicated user"})
    try:
        user = User(
            name=in_json["name"],
            email=in_json["email"]
        )
        user.set_password(in_json["password"])
        db_sess.add(user)
        db_sess.commit()
        return create_jwt_for_user(user)
    except Exception:
        return jsonify({"error": "Bad request"})


# ----авторизация зарегистрированного пользователя----
@blueprint.route('/api/login', methods=["GET"])
def login_user():
    in_json = request.json  # получаем json, отправленный клиентом (словарь)
    # request - запрос
    if not in_json:  # если в json пусто
        return jsonify({"error": "Empty request"})
    elif not check_keys(in_json, ("email", 'password')):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == in_json['email']).first()
    if user is None:
        return jsonify({'error': 'User not found'})
    return create_jwt_for_user(user)


# ----получить задачи пользоваателя----
@blueprint.route('/api/users/tasks', methods=["GET"])
@jwt_required
def get_user_tasks():
    tasks_data = []
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == get_jwt_identity()["email"]).first()

    for task_id in user.tasks.split():
        print(task_id)
        task = db_sess.query(Task).filter(Task.id == int(task_id)).first()
        print(task)
        tasks_data.append({"id": task.id, "title": task.title, "complete": task.complete,
                           "description": task.description, "creation_date": task.creation_date,
                           "deadline": task.deadline, "files": task.files})
    tasks_data.reverse()
    return jsonify({"tasks": tasks_data})


@blueprint.route('/api/tasks/new', methods=["POST"])
@jwt_required
def create_new_task():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not 'title' in request.json.keys():
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == get_jwt_identity()["email"]).first()
    task = db_sess.query(Task).filter(Task.title == request.json['title']).first()
    if task:
        return jsonify({"error": "Task already exists"})
    task = Task()
    task.title = request.json['title']
    # добавляем другие параметры, если они есть
    if "complete" in request.json.keys():
        task.complete = request.json['complete']
    if "description" in request.json.keys():
        task.description = request.json['description']
    if "deadline" in request.json.keys():
        task.deadline = request.json['deadline']
    if "files" in request.json.keys():
        task.files = request.json['files']

    db_sess.add(task)
    db_sess.commit()
    task = db_sess.query(Task).filter(Task.title == request.json['title']).first()
    user.tasks += " " + str(task.id)
    db_sess.commit()
    return jsonify({"message": "success"})


@blueprint.route('/api/tasks/delete', methods=["DELETE"])
@jwt_required
def delete_task():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not 'title' in request.json.keys():
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == get_jwt_identity()["email"]).first()
    task = db_sess.query(Task).filter(Task.title == request.json['title']).first()
    if not task:
        return jsonify({"error": "Task does not exists"})
    db_sess.delete(task)  # todo
    db_sess.commit()
    print(user.tasks)
    print(type(user.tasks))
    user.tasks = user.tasks.replace(str(task.id), "", 1)
    # data = user.tasks.split()
    # data.remove(str(task.id))
    # user.tasks = data
    db_sess.commit()
    return jsonify({"message": "success"})


@blueprint.route('/api/tasks/change/<int:task_id>', methods=["POST"])
@jwt_required
def change_task(task_id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).filter(Task.id == task_id).first()
    if not task:
        return jsonify({"error": "Task not found"})
    # добавляем параметры, если они есть
    # if "complete" in request.json.keys():
    #     task.complete = request.json['complete']
    # if "description" in request.json.keys():
    #     task.description = request.json['description']
    # if "deadline" in request.json.keys():
    #     task.deadline = request.json['deadline']
    # if "files" in request.json.keys():
    #     task.files = request.json['files']
    task.complete = not task.complete
    db_sess.commit()
    return jsonify({"message": "success"})


@blueprint.route('/api/files/add', methods=["POST"])
@jwt_required
def add_file():
    pass  # todo загрузка файлов

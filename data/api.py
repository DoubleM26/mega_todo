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
    # if not request.json:
    #     return jsonify({"error": "Empty request"})
    # elif not check_keys(request.json, ())

# это для примера
# @app.route("/api/posts", methods=["POST"])
# @jwt_required
# def add_post():
#     if not request.json:
#         return make_resp(jsonify({"message":"Empty request"}), 400)
#     elif not check_keys(request.json, ("category", "type", "titile")):
#         return make_resp(jsonify({"message":"bad request"}), 400)
#     post = Post(**request.json)
#     post.author = User(**get_jwt_identify())
#     post=app.post_repo.request_create(post)
#     return make_resp(jsonify(post), 200)


# @blueprint.route('/api/users/<int:user_id>/tasks', methods=['GET'])
# def get_user_tasks(user_id):
#     db_sess = db_session.create_session()
#     tasks = db_sess.query(Task).get(user_id)
#     if not tasks:
#         return jsonify({'error': 'Not found'})
#     return jsonify(
#         {
#             'tasks': tasks.to_dict(only=(
#                 'id', 'title', 'complete', 'description', 'creation_date', 'deadline', 'files'))
#         }
#     )


# # todo нужно сначала зарегистрироваться, чтобы загружать новые задачи
# @blueprint.route('/api/users/<int:user_id>/tasks', methods=['POST'])
# def create_tasks(user_id):
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['title', 'content', 'user_id', 'is_private']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     task = Task(
#         id=-1
#     )  # todo
#     db_sess.add(task)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
#
# @blueprint.route('/api/users/<int:user_id>/tasks/<int:news_id>', methods=['DELETE'])
# def delete_tasks(news_id):
#     db_sess = db_session.create_session()
#     task = db_sess.query(Task).get(news_id)
#     if not task:
#         return jsonify({'error': 'Not found'})
#     db_sess.delete(task)
#     # todo удаляется так-же и у пользователя
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
# # todo - изменение задачи

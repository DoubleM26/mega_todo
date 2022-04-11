import flask
from flask import jsonify, request

from data import db_session
from data.User import User
from data.Task import Task

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


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


@blueprint.route('/api/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).get(user_id)
    if not tasks:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'tasks': tasks.to_dict(only=(
                'id', 'title', 'complete', 'description', 'creation_date', 'deadline', 'files'))
        }
    )


# todo нужно сначала зарегистрироваться, чтобы загружать новые задачи
@blueprint.route('/api/users/<int:user_id>/tasks', methods=['POST'])
def create_tasks(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    task = Task(
        id=-1
    )  # todo
    db_sess.add(task)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>/tasks/<int:news_id>', methods=['DELETE'])
def delete_tasks(news_id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(news_id)
    if not task:
        return jsonify({'error': 'Not found'})
    db_sess.delete(task)
    # todo удаляется так-же и у пользователя
    db_sess.commit()
    return jsonify({'success': 'OK'})

# todo - изменение задачи

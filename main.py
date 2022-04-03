from flask import Flask, make_response, jsonify, render_template
from forms.login import LoginForm
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    return render_template("intro.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form, title="Авторизация")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # db_session.global_init("db/super_todo.db")
    # app.register_blueprint(api.blueprint)
    app.run(port=8080, host='127.0.0.1')


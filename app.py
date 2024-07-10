from flask import Flask, session, g
from exts import db, mail
from models import UserModel
from flask_migrate import Migrate
from blueprints.qa import bp as qa
from blueprints.auth import bp as auth
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa)
app.register_blueprint(auth)


# 钩子函数
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()

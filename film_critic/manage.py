from app import create_app, db
from app.models import User, Tag, Comment, Movie, UsersMoviesEvaluates, UsersCommentsEvaluates, Blog, Message
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os


app = create_app(os.getenv('PJ_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Tag=Tag, Movie=Movie, Comment=Comment,
                UsersMoviesEvaluates=UsersMoviesEvaluates, UsersCommentsEvaluates=UsersCommentsEvaluates, Blog=Blog, Message=Message)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

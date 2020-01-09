from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from app import app
from note.extensions import db

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()

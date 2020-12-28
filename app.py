from flask import Flask
from flask_migrate import Migrate
from DatabaseCreate import database


programm = Flask(__name__)

programm.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
programm.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.__init__(programm)
migrate = Migrate(programm, database)


if __name__ == '__main__':
    programm.run()

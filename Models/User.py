from DatabaseCreate import database


class User(database.Model):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    userName = database.Column(database.String(50), unique=True)
    firstName = database.Column(database.String(30))
    lastName = database.Column(database.String(30))
    email = database.Column(database.String(50))
    password = database.Column(database.String(20))
    phone = database.Column(database.String(10))
    userStatusModerator = database.Column(database.Boolean)

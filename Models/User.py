from DatabaseCreate import database
from re import *


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

    def __init__(self,
                 userName=None,
                 firstName=None,
                 lastName=None,
                 email=None,
                 password=None,
                 phone=None,
                 userStatusModerator=False):
        self.userName=userName
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.password=password
        self.phone=phone
        self.userStatusModerator=userStatusModerator

    def SomeEmptyFields(self):
        if not self.userName or not self.firstName or not self.lastName :
            return True
        if not self.email or not self.phone or not self.password:
            return True
        return False

    def InvalidInput(self):
        name = compile('(^|\s)(\w){2,30}(\s|$)')
        phone = compile('(^|\s)(0)+(\d){9}(\s|$)')
        email = compile('(^|\s)[-a-z|0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        if not  name.match(self.userName) or not name.match(self.firstName) or not name.match(self.lastName):
            return True
        if not phone.match(self.phone):
            return True
        if not email.match(self.email):
            return True
        return False

    @classmethod
    def ReadFromDatabase(cls, user_id=None,userName=None):
        if user_id:
            return User.query.filter_by(id=user_id).first()
        if userName:
            return User.query.filter_by(userName=userName).first()
        return None
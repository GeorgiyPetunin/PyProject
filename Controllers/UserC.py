from Models.User import User
from werkzeug.security import generate_password_hash
from DatabaseCreate import database
from flask import jsonify


class UserController(object):

    def __init__(self, user=User()):
        self.user = user

    def Create(self, user_data=None):
        self.user=User()
        self.user.userName = user_data.get('userName')
        self.user.firstName = user_data.get('firstName')
        self.user.lastName = user_data.get('lastName')
        self.user.email = user_data.get('email')
        self.user.phone = user_data.get('phone')
        if user_data.get('moderator')=='moderator':
            self.user.userStatusModerator = 1
        if user_data.get('password'):
            self.user.password = generate_password_hash(user_data.get('password'))

        if self.user.SomeEmptyFields():
            return jsonify(message='Not all fields was filled!', status=400)
        if self.user.InvalidInput():
            return jsonify(message='Invalid data input!', status=400)
        if User.ReadFromDatabase(userName=self.user.userName):
            return jsonify(message='User with this name already exist!', status=409)

        database.session.add(self.user)
        database.session.commit()
        return jsonify(message='Successfully user creation!', status=200)

    def Read(self, user_id=None):
        readUser= User.ReadFromDatabase(user_id=user_id)
        if readUser:
            return jsonify(message = [readUser.userName,
                                        readUser.firstName,
                                        readUser.lastName,
                                        readUser.email,
                                        readUser.phone,
                                        readUser.userStatusModerator],status=200)
        else:
            return jsonify(message='No user with such id!', status=404)

    def Edit(self, user_id=None,user_data=None):

        self.user=User.ReadFromDatabase(user_id=user_id)
        self.user.id = user_id
        if user_data.get('new_userName') and self.user.userName != user_data.get('new_userName'):

            if User.ReadFromDatabase(userName=self.user.userName) and self.user!=User.ReadFromDatabase(userName=self.user.userName):
                return jsonify(message='User with this name already exist!', status=409)
            self.user.userName = user_data.get('new_userName')
        if user_data.get('new_firstName'):
            self.user.firstName = user_data.get('new_firstName')
        if user_data.get('new_lastName'):
            self.user.lastName = user_data.get('new_lastName')
        if user_data.get('new_email'):
            self.user.email = user_data.get('new_email')
        if user_data.get('new_phone'):
            self.user.phone = user_data.get('new_phone')
        if user_data.get('new_password'):
            self.user.password = generate_password_hash(user_data.get('new_password'))

        if self.user.InvalidInput():
            return jsonify(message='Invalid data input!', status=400)

        database.session.commit()
        return jsonify(message='Successfully user edition!', status=200)

    def Delete(self, user_id=None):
        readUser= User.ReadFromDatabase(user_id=user_id)
        if readUser:
            database.session.delete(readUser)
            database.session.commit()
            return jsonify(message='Successfully user delete!', status=200)
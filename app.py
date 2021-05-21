import base64
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, make_response, abort
from flask_migrate import Migrate
from DatabaseCreate import database
from werkzeug.security import check_password_hash
from flask_marshmallow import Marshmallow
from functools import wraps
import datetime, jwt
from flask_cors import CORS

def g_header(username, password):
    return base64.b64encode(
        '{username}:{password}'.format(
            username=username,
            password=password).encode()
    ).decode()

programm = Flask(__name__)
programm.config['SECRET_KEY'] = 'my special secret  key'
programm.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
programm.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.__init__(programm)
migrate = Migrate(programm, database)
test_programm = programm.test_client()
ma = Marshmallow(programm)
cors = CORS(programm, resources ={
    r"/*" : {
        "origins": "*"
    }
})
bcrypt = Bcrypt(programm)


@programm.route('/api/v1/hello-world-22')
def hello_world():
    return 'Hello World 22 !'


from Controllers.UserC import UserController, user_schema
from Controllers.ArticleC import ArticleController
from Controllers.EditProposeC import EditProposeController
from Models.User import User, UserSchema
from flask import request

# jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjA5MTg1MzE3fQ.KqAC2V5l2_Oz0AY_IVxAhMXunh0A8dV6jocExeHMiPs','my special secret key')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print(token)
        if not token:
            return jsonify(message='Token is missing!', status=401)
        try:
            data = jwt.decode(token, 'my special secret  key')
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify(message='Token is invalid!', status=401)

        return f(current_user, *args, **kwargs)

    return decorated

@programm.route("/Login", methods=['GET'])
def login():
    userName = request.args.get('userName')
    password = request.args.get('password')
    user = User.query.filter_by(userName=userName).first()
    print(user)
    if user is not None:
        user_data = user_schema.dump(user)
        if bcrypt.check_password_hash(user.password, password):
            response = make_response(
                jsonify(
                    {"user": UserSchema().load(user_data),
                     "token": g_header(userName, password)}
                ), 200
            )
            response.headers["Content-Type"] = "application/json"
            return response
    return jsonify(message='Wrong username or password'), 403

# @programm.route('/Login')
# def login():
#     data = request.authorization
#     if not data or not data.username or not data.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#     user = User.query.filter_by(userName=data.username).first()
#     if not user:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#
#     if check_password_hash(user.password, data.password):
#         token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
#                            'my special secret  key')
#         return jsonify({'token': token.decode('utf-8'), 'user_id': user.id})
#
#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# http://127.0.0.1:5000/User?userName=olegdupa&firstName=oleg&lastName=dupa&email=olegdupa@gmail.com&phone=0976666666&moderator=moderator&password=dupa
@programm.route('/User', methods=['POST'])
def createUser():
    userController = UserController()
    return userController.Create(user_data=request.args)


# http://127.0.0.1:5000/User
@programm.route('/User', methods=['GET'])
@token_required
def readUser(current_user):
    userController = UserController()
    return userController.Read(user_id=current_user.id)


# # http://127.0.0.1:5000/User?new_userName=olegdupa&new_firstName=oleg&new_lastName=duPa&new_email=olegdupa@gmail.com&new_phone=0976666666&new_password=dupa
# @programm.route('/User', methods=['PUT'])
# @token_required
# def editUser(current_user):
#     userController = UserController()
#     return userController.Edit(user_id=current_user.id, user_data=request.args)

@programm.route("/User/<string:userName>", methods=['PUT'])
def user_update(userName):
    user_up = User.query.filter_by(userName=userName).first()
    if user_up is None:
        return abort(404, 'user not found')
    try:
        user_up.firstName = request.json['firstName']
        user_up.lastName = request.json['lastName']
        user_up.email = request.json['email']
        user_up.phone = request.json['phone']
        password = request.json['password']
        if not bcrypt.check_password_hash(user_up.password, password) and password!='':
            user_up.password = bcrypt.generate_password_hash(password)
        database.session.commit()
        return user_schema.jsonify(user_up)
    except:
        return abort(405, 'Error')

# http://127.0.0.1:5000/User
# @programm.route('/User', methods=['DELETE'])
# @token_required
# def deleteUser(current_user):
#     userController = UserController()
#     return userController.Delete(user_id=current_user.id)

@programm.route('/User/<string:userName>', methods=['DELETE'])
def deleteUser(userName):
    if User.query.filter_by(userName=userName).first() is None:
        abort(404, 'No such user in database')
    try:
        userToDelete = User.query.filter_by(userName=userName).first()
        database.session.delete(userToDelete)
        database.session.commit()
    except:
        abort(404, 'User not found')
    return 'User deleted successfully', 200


# http://127.0.0.1:5000/ArticleAll
@programm.route('/ArticleAll', methods=['GET'])
def readArticleAll():
    articleController = ArticleController()
    return articleController.Read()


# http://127.0.0.1:5000/ArticleU
@programm.route('/ArticleU', methods=['GET'])
@token_required
def readArticleUser(current_user):
    articleController = ArticleController()
    return articleController.Read(user_id=current_user.id)


# http://127.0.0.1:5000/Article?id=1
@programm.route('/Article', methods=['GET'])
def readArticle():
    articleController = ArticleController()
    return articleController.Read(article_id=request.args.get('id'))


# http://127.0.0.1:5000/ArticleEdit?text=for_purpose&article_id=1
@programm.route('/ArticleEdit', methods=['POST'])
@token_required
def createEditPurpose(current_user):
    editProposeController = EditProposeController()
    return editProposeController.Create(user_id=current_user.id, edit_data=request.args)


# http://127.0.0.1:5000/EditPropose?propose_id=1
@programm.route('/EditPropose', methods=['GET'])
@token_required
def readPropose(current_user):
    editProposeController = EditProposeController()
    return editProposeController.Read(user_id=current_user.id, propose_id=request.args.get('propose_id'))


# http://127.0.0.1:5000/EditProposeAll
@programm.route('/EditProposeAll', methods=['GET'])
@token_required
def readProposeAll(current_user):
    editProposeController = EditProposeController()
    return editProposeController.Read(user_id=current_user.id)


# http://127.0.0.1:5000/ProposeDecision?propose_id=1&decision=edit
@programm.route('/ProposeDecision', methods=['PUT'])
@token_required
def proposeDecision(current_user):
    editProposeController = EditProposeController()
    return editProposeController.Decision(user_id=current_user.id, propose_data=request.args)


if __name__ == '__main__':
    programm.run()

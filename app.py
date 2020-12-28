from flask import Flask
from flask_migrate import Migrate
from DatabaseCreate import database


programm = Flask(__name__)

programm.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
programm.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.__init__(programm)
migrate = Migrate(programm, database)


@programm.route('/api/v1/hello-world-22')
def hello_world():
    return 'Hello World 22 !'


from Controllers.UserC import UserController
from Controllers.ArticleC import ArticleController
from Controllers.EditProposeC import EditProposeController
from flask import request



# http://127.0.0.1:5000/User?userName=olegdupa&firstName=oleg&lastName=dupa&email=olegdupa@gmail.com&phone=0976666666&moderator=moderator&password=dupa
@programm.route('/User',methods=['POST'])
def createUser():
    userController=UserController()
    return userController.Create(user_data=request.args)

# http://127.0.0.1:5000/User?id=1
@programm.route('/User',methods=['GET'])
def readUser():
    userController = UserController()
    return userController.Read(user_id=request.args.get('id'))

# http://127.0.0.1:5000/User?new_userName=olegdupa&new_firstName=oleg&new_lastName=duPa&new_email=olegdupa@gmail.com&new_phone=0976666666&new_password=dupa&id=1
@programm.route('/User',methods=['PUT'])
def editUser():
    userController=UserController()
    return userController.Edit(user_id=request.args.get('id'),user_data=request.args)

# http://127.0.0.1:5000/User?id=1
@programm.route('/User',methods=['DELETE'])
def deleteUser():
    userController = UserController()
    return userController.Delete(user_id=request.args.get('id'))

# http://127.0.0.1:5000/Article?id=1&name=target&text=smth about target
@programm.route('/Article', methods=['POST'])
def createArticle():
    articleController=ArticleController()
    return articleController.Create(user_id=request.args.get('id'),article_data=request.args)

# http://127.0.0.1:5000/ArticleAll
@programm.route('/ArticleAll', methods=['GET'])
def readArticleAll():
    articleController=ArticleController()
    return articleController.Read()

# http://127.0.0.1:5000/ArticleU?id=1
@programm.route('/ArticleU', methods=['GET'])
def readArticleUser():
    articleController=ArticleController()
    return articleController.Read(user_id=request.args.get('id'))

# http://127.0.0.1:5000/Article?id=1
@programm.route('/Article', methods=['GET'])
def readArticle():
    articleController=ArticleController()
    return articleController.Read(article_id=request.args.get('id'))

# http://127.0.0.1:5000/ArticleEdit?id=1&text=for_purpose&article_id=1
@programm.route('/ArticleEdit', methods=['POST'])
def createEditPurpose():
    editProposeController=EditProposeController()
    return editProposeController.Create(user_id=request.args.get('id'),edit_data=request.args)

# http://127.0.0.1:5000/EditPropose?id=1&propose_id=1
@programm.route('/EditPropose',methods=['GET'])
def readPropose():
    editProposeController = EditProposeController()
    return editProposeController.Read(user_id=request.args.get('id'),propose_id=request.args.get('propose_id'))

# http://127.0.0.1:5000/EditProposeAll?id=1
@programm.route('/EditProposeAll',methods=['GET'])
def readProposeAll():
    editProposeController = EditProposeController()
    return editProposeController.Read(user_id=request.args.get('id'))

# http://127.0.0.1:5000/ProposeDecision?id=1&propose_id=1&decision=edit
@programm.route('/ProposeDecision',methods=['PUT'])
def proposeDecision():
    editProposeController = EditProposeController()
    return editProposeController.Decision(user_id=request.args.get('id'),propose_data=request.args)

if __name__ == '__main__':
    programm.run()

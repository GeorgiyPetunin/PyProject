import pytest
from app import programm, test_programm
from Models.User import User
from Models.Article import Article
from Models.EditPropose import EditPropose
import jwt, datetime
from copy import copy


# pytestmark = pytest.mark.random_order(disabled=False)

class TestData():
    user_data = {
        'userName': 'ivanfranko',
        'firstName': 'ivan',
        'lastName': 'franko',
        'email': 'ivanfranko@gmail.com',
        'phone': '0977417415',
        'password': 'ivan'
    }
    user_data_moderator = {
        'userName': 'johanbah',
        'firstName': 'johan',
        'lastName': 'bach',
        'email': 'johanbach@gmail.com',
        'moderator': 'moderator',
        'phone': '0977485177',
        'password': 'johan'
    }
    user_data_for_update = {
        'new_userName': 'IvanFranko',
        'new_firstName': 'Ivan',
        'new_lastName': 'Franko',
        'new_email': 'ivanfranko@gmail.com',
        'new_phone': '0977417415',
        'new_password': 'ivan'
    }
    article_data = {
        'text': 'some test text',
        'name': 'test name'
    }
    edit_propose_data = {
        'text': 'some new text',
        'article_id': '1'
    }


userID = 0


@pytest.fixture()
def autorised():
    programm.testing = True
    client = programm.test_client()
    global token
    print(userID)
    token = jwt.encode({'id': userID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                       programm.config['SECRET_KEY'])
    yield client
    programm.testing = False


def create_args(args):
    line = ''
    for i in args:
        line += '&' + i + '=' + args[i]
    return '?' + line[1:]


# CREATE USER

# empty fields
@pytest.mark.order(1)
def test_createUserEmptyFields():
    data = copy(TestData.user_data)
    data['firstName'] = ''
    data = create_args(data)
    run = test_programm.post('/User' + data)
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Not all fields was filled!",
        'status': 400
    }


# invalid data
@pytest.mark.order(2)
def test_createUserInvalidData():
    data = copy(TestData.user_data)
    data['phone'] = '095745K853'
    data = create_args(data)
    run = test_programm.post('/User' + data)
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Invalid data input!",
        'status': 400
    }


# right test
@pytest.mark.order(3)
def test_createUser1():
    data = copy(TestData.user_data)
    data = create_args(data)
    run = test_programm.post('/User' + data)
    print('created!')
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully user creation!",
        'status': 200
    }


# user with such name exist
@pytest.mark.order(4)
def test_createUserNonUnique():
    data = copy(TestData.user_data)
    data = create_args(data)
    run = test_programm.post('/User' + data)
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "User with this name already exist!",
        'status': 409
    }


# right test 2
@pytest.mark.order(5)
def test_createUser2():
    data = copy(TestData.user_data_moderator)
    data = create_args(data)
    run = test_programm.post('/User' + data)
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully user creation!",
        'status': 200
    }


# LOGIN

# empty fields
@pytest.mark.order(6)
def test_loginEmptyFields():
    data = {
        'password': TestData.user_data['password']
    }
    data = create_args(data)
    run = test_programm.get('/Login' + data)
    assert run.status_code == 401


# non existing user
@pytest.mark.order(7)
def test_loginNonUser():
    data = {
        'userName': 'NonExistingUser',
        'password': 'password'
    }
    data = create_args(data)
    run = test_programm.get('/Login' + data)
    assert run.status_code == 401


# bad password
@pytest.mark.order(8)
def test_loginBadPassword():
    data = {
        'userName': TestData.user_data['userName'],
        'password': 'WrongPassword'
    }
    data = create_args(data)
    run = test_programm.get('/Login' + data)
    assert run.status_code == 401


@pytest.fixture()
def setUserID():
    global userID
    userID = User.query.filter_by(userName=TestData.user_data['userName']).first().id


@pytest.fixture()
def setUserIDModerator():
    global userID
    print()
    userID = User.query.filter_by(userName=TestData.user_data_moderator['userName']).first().id


# READ USER

# right test
@pytest.mark.order(10)
def test_readUser(setUserID, autorised):
    run = test_programm.get('/User', headers={'x-access-token': token})
    assert run.status_code == 200


# Token missing
@pytest.mark.order(11)
def test_readUserTokenMissing(setUserIDModerator, autorised):
    run = test_programm.get('/User')
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Token is missing!",
        'status': 401
    }


# wrong token
@pytest.mark.order(12)
def test_readUserTokenError(setUserID, autorised):
    run = test_programm.get('/User', headers={'x-access-token': '8grgvdrjhe6dr6ru6svysy4'})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Token is invalid!",
        'status': 401
    }


# EDIT USER

# right test
def test_editUser(setUserID, autorised):
    data = copy(TestData.user_data_for_update)
    data = create_args(data)
    run = test_programm.put('/User' + data, headers={'x-access-token': token})
    TestData.user_data['userName'] = TestData.user_data_for_update['new_userName']
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully user edition!",
        'status': 200
    }


# CREATE ARTICLE

# empty fields
def test_createArticleEmptyFields(setUserID, autorised):
    data = copy(TestData.article_data)
    data['name'] = ''
    data = create_args(data)
    run = test_programm.post('/Article' + data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Not all fields was filled!",
        'status': 400
    }


# right test
def test_createArticle(setUserID, autorised):
    data = copy(TestData.article_data)
    data = create_args(data)
    run = test_programm.post('/Article' + data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully article creation!",
        'status': 200
    }


# READ ALL ARTICLES

# right test
def test_readAllArticles():
    run = test_programm.get('/ArticleAll')
    assert run.status_code == 200


# READ ARTICLE

# bad id
def test_readArticleBadID():
    run = test_programm.get('/Article?id=9999')
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "No article with such id!",
        'status': 404
    }


# right test
def test_readArticle():
    data = {
        'id': str(Article.query.filter_by().first())
    }
    data = create_args(data)
    run = test_programm.get('/Article')
    assert run.status_code == 200


# READ ARTICLE BY USER

# right test
def test_readArticleUser(setUserID, autorised):
    run = test_programm.get('/ArticleU', headers={'x-access-token': token})
    assert run.status_code == 200


# CREATE PROPOSE

# empty fields
def test_createProposeEmptyFields(setUserID, autorised):
    data = copy(TestData.edit_propose_data)
    data['text'] = ''
    data = create_args(data)
    run = test_programm.post('/ArticleEdit' + data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Not all fields was filled!",
        'status': 400
    }


# bad id
def test_createProposeBadID(setUserID, autorised):
    data = copy(TestData.edit_propose_data)
    data['article_id'] = '99999'
    data = create_args(data)
    run = test_programm.post('/ArticleEdit' + data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "No article with such id!",
        'status': 404
    }


# right test
def test_createPropose(setUserID, autorised):
    data = copy(TestData.edit_propose_data)
    data = create_args(data)
    run = test_programm.post('/ArticleEdit' + data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully edit propose creation!",
        'status': 200
    }


# READ ALL PROPOSES

# not admitions
def test_readProposeNoAdmitions(setUserID, autorised):
    run = test_programm.get('/EditProposeAll', headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "You do not have admitions!",
        'status': 403
    }


# bad id
def test_readProposeBadID(setUserIDModerator, autorised):
    run = test_programm.get('/EditPropose?propose_id=999999', headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "No propose with such id!",
        'status': 404
    }


# right test
def test_readPropose(setUserIDModerator, autorised):
    run = test_programm.get('/EditPropose?propose_id=1', headers={'x-access-token': token})
    assert run.status_code == 200


# PROPOSE DECISION

# not admitions
def test_ProposeDecisionNoAdmitions(setUserID, autorised):
    run = test_programm.put('/ProposeDecision', headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "You do not have admitions!",
        'status': 403
    }

# bad id
def test_ProposeDecisionBadID(setUserIDModerator, autorised):
    data={
        'propose_id':'999999',
        'decision':'edit'
    }
    data=create_args(data)
    run = test_programm.put('/ProposeDecision'+data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "No propose with such id!",
        'status': 404
    }

# right test
def test_ProposeDecisionEdit(setUserIDModerator, autorised):
    data={
        'propose_id':str(EditPropose.query.filter_by(complete=0).first().id),
        'decision':'edit'
    }
    data=create_args(data)
    run = test_programm.put('/ProposeDecision'+data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully article edition!",
        'status': 200
    }

# right test
def test_ProposeDecisionDiscard(setUserIDModerator, autorised):
    data={
        'propose_id':str(EditPropose.query.filter_by(complete=0).first().id),
        'decision':'discard'
    }
    data=create_args(data)
    run = test_programm.put('/ProposeDecision'+data, headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully edition discard!",
        'status': 200
    }

# DELETE USER

# right test
def test_deleteUser1(setUserID, autorised):
    run = test_programm.delete('/User', headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully user delete!",
        'status': 200
    }


# right test 2
def test_deleteUser2(setUserIDModerator, autorised):
    run = test_programm.delete('/User', headers={'x-access-token': token})
    assert run.status_code == 200
    assert run.get_json() == {
        'message': "Successfully user delete!",
        'status': 200
    }

# coverage run --omit 'venv/*' -m pytest -q Tests.py
# coverage report --omit 'venv/*' -m

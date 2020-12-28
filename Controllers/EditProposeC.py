from Models.EditPropose import EditPropose
from Models.User import User
from Models.Article import Article
from flask import jsonify
from DatabaseCreate import database


class EditProposeController(object):

    def __init__(self, edit_propose=EditPropose()):
        self.edit_propose = edit_propose

    def Create(self, user_id=None, edit_data=None):
        readUser = User.ReadFromDatabase(user_id=user_id)
        if not readUser:
            return jsonify(message='No user with such id!', status=404)
        self.edit_propose.editor = readUser

        readArticle = Article.ReadFromDatabase(article_id=edit_data.get('article_id'))
        if not readArticle:
            return jsonify(message='No article with such id!', status=404)
        self.edit_propose.article_id = readArticle.id

        self.edit_propose.text = edit_data.get('text')
        if self.edit_propose.SomeEmptyFields():
            return jsonify(message='Not all fields was filled!', status=400)

        database.session.add(self.edit_propose)
        database.session.commit()
        return jsonify(message='Successfully edit propose creation!', status=200)

    def Read(self, user_id=None, propose_id=None):
        current_user = User.ReadFromDatabase(user_id=user_id)
        if not current_user.userStatusModerator:
            return jsonify(message='You do not have admitions!', status=403)
        if propose_id:
            read_propose = EditPropose.ReadFromDatabase(propose_id=propose_id)
            if not read_propose:
                return jsonify(message='No propose with such id!', status=404)
            return jsonify(message=[read_propose.text, read_propose.editor_id, read_propose.article_id], status=200)
        list_propose = EditPropose.ReadFromDatabase()
        return jsonify(list =[[i.text, i.editor_id, i.article_id] for i in list_propose], status=200)


    def Decision(self, user_id=None, propose_data=None):
        current_user = User.ReadFromDatabase(user_id=user_id)
        if not current_user.userStatusModerator:
            return jsonify(message='You do not have admitions!', status=403)
        propose_id = propose_data.get('propose_id')
        if propose_id:
            read_propose = EditPropose.ReadFromDatabase(propose_id=propose_id)
            if not read_propose:
                return jsonify(message='No propose with such id!', status=404)
            self.edit_propose = read_propose
        decision = propose_data.get('decision')
        if decision == 'edit':
            article = Article.ReadFromDatabase(article_id=read_propose.article_id)
            article.text = read_propose.text
            database.session.commit()
            self.Delete()
            return jsonify(message='Successfully article edition!', status=200)
        if decision == 'discard':
            self.Delete()
            return jsonify(message='Successfully edition discard!', status=200)

    def Delete(self):
        database.session.delete(self.edit_propose)
        database.session.commit()

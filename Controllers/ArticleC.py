from Models.Article import Article
from Models.User import User
from DatabaseCreate import database
from flask import jsonify


class ArticleController(object):

    def __init__(self, article=Article()):
        self.article=article

    def Create(self, user_id=None,article_data=None):
        self.article=Article()
        readUser = User.ReadFromDatabase(user_id=user_id)

        self.article.creator=readUser
        self.article.text=article_data.get('text')
        self.article.name=article_data.get('name')
        if self.article.SomeEmptyFields():
            return jsonify(message='Not all fields was filled!', status=400)

        database.session.add(self.article)
        database.session.commit()
        return jsonify(message='Successfully article creation!', status=200)

    def Read(self,user_id=None,article_id=None):
        if user_id:
            list_of_articles = Article.ReadFromDatabase(user_id=user_id)
            return jsonify(list=[[i.text,i.name]for i in list_of_articles], status=200)
        if article_id:
            readArticle = Article.ReadFromDatabase(article_id=article_id)
            if readArticle==None:
                return jsonify(message='No article with such id!', status=404)
            return jsonify(message=[readArticle.name,
                                    readArticle.text],status=200)
        list_of_articles = Article.ReadFromDatabase()
        return jsonify(list=[[i.text, i.name,i.creator_id] for i in list_of_articles], status=200)


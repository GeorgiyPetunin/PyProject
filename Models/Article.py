from DatabaseCreate import database
from Models.User import User


class Article(database.Model):
    __tablename__ = 'article'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50))
    text = database.Column(database.String(2000))
    creator_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    creator = database.relationship('User', backref='user')

    def __init__(self,
                 name=None,
                 text=None,
                 creator=None):
        self.name=name
        self.text=text
        self.creator=creator

    def SomeEmptyFields(self):
        if not self.name or not self.text:
            return True
        return False

    @classmethod
    def ReadFromDatabase(cls, user_id=None, article_id=None):
        if user_id:
            return Article.query.filter_by(creator_id=user_id)
        if article_id:
            return Article.query.filter_by(id=article_id).first()
        return Article.query.all()


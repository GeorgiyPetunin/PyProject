from DatabaseCreate import database


class Article(database.Model):
    __tablename__ = 'article'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50))
    text = database.Column(database.String(2000))
    creator_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    creator = database.relationship('User', backref='user')

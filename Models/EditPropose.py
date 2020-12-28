from DatabaseCreate import database


class EditPropose(database.Model):
    __tablename__ = 'editpropose'

    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String(2000))
    complete = database.Column(database.Boolean)
    editor_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    editor = database.relationship('User', backref='user')
    article_id = database.Column(database.Integer)
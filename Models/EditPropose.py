from DatabaseCreate import database


class EditPropose(database.Model):
    __tablename__ = 'editpropose'

    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String(2000))
    complete = database.Column(database.Boolean)
    editor_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    editor = database.relationship('User', backref='User')
    article_id = database.Column(database.Integer)

    def __init__(self,
                 text=None,
                 complete=False,
                 editor=None,
                 article_id=None):
        self.text = text
        self.complete = complete
        self.editor = editor
        self.article_id = article_id

    def SomeEmptyFields(self):
        if not self.text:
            return True
        return False

    @classmethod
    def ReadFromDatabase(cls, propose_id=None):
        if propose_id:
            return EditPropose.query.filter_by(id=propose_id).first()
        return EditPropose.query.all()

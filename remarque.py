from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.rest import RestAPI, UserAuthentication
from peewee import CharField, TextField, DateTimeField
import times

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db = Database(app)
auth = Auth(app, db)

class Note(db.Model):
    title = CharField()
    content = TextField()
    created = DateTimeField(default=times.now)

class NoteAdmin(ModelAdmin):
    columns = ('title', 'content', 'created',)

admin = Admin(app, auth)
admin.register(Note, NoteAdmin)
auth.register_admin(admin)
admin.setup()

user_auth = UserAuthentication(auth)
api = RestAPI(app, default_auth=user_auth)
api.register(Note)
api.setup()

if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Note.create_table(fail_silently=True)
    app.run()

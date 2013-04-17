from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth, BaseUser
from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.rest import RestAPI, RestResource, RestrictOwnerResource, UserAuthentication, AdminAuthentication
from peewee import CharField, TextField, DateTimeField, BooleanField, ForeignKeyField
import times

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db = Database(app)


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=times.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

class Note(db.Model):
    user = ForeignKeyField(User)
    title = CharField()
    content = TextField()
    created = DateTimeField(default=times.now)

class NoteAdmin(ModelAdmin):
    columns = ('title', 'content', 'created',)

class UserAdmin(ModelAdmin):
    columns = ('username', 'email', 'admin', )

class CustomAuth(Auth):
    def get_user_model(self):
        return User

    def get_model_admin(self, model_admin=None):
        return UserAdmin

auth = CustomAuth(app, db)

admin = Admin(app, auth)
admin.register(Note, NoteAdmin)
admin.register(User, UserAdmin)
auth.register_admin(admin)
admin.setup()

class UserResource(RestResource):
    exclude = ('password', 'email',)

class NoteResource(RestrictOwnerResource):
    owner_field = 'user'

user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)
api.register(User, UserResource, auth=admin_auth)
api.register(Note, NoteResource)
api.setup()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config["PORT"])

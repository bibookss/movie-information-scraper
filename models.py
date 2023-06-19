from peewee import *
from playhouse.sqlite_ext import *
from dotenv import dotenv_values

config = dotenv_values('.env')

_host = config['HOST']
_user = config['USER']
_password = config['PASSWORD']
_database = config['DATABASE']

db = MySQLDatabase(database, host=_host, user=_user, password=_password)

class BaseModel(Model):
    class Meta:
        database = db

class Genre(BaseModel):
    name = CharField(unique=True)
    
class Movie(BaseModel):
    name = CharField()
    url = CharField(unique=True)
    description = TextField(default=None)
    certification = CharField(default=None)
    release = DateField(default=None)
    genres = ManyToManyField(Genre)
    is_visited = BooleanField(default=False)
    
class Website(BaseModel):
    url = CharField(unique=True)
    is_visited = BooleanField(default=False)

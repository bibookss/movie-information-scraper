from peewee import *
from playhouse.sqlite_ext import *
from dotenv import dotenv_values

config = dotenv_values('.env')

_host = config['HOST']
_user = config['USER']
_password = config['PASSWORD']
_database = config['DATABASE']

db = MySQLDatabase(_database, host=_host, user=_user, password=_password)

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
    is_visited = BooleanField(default=False)
    genres = ManyToManyField(Genre, backref='movies')
    duration = IntegerField()

class Website(BaseModel):
    url = CharField(unique=True)
    is_visited = BooleanField(default=False)

MovieGenre = Movie.genres.get_through_model()

db.create_tables([Genre, Movie, MovieGenre, Website])


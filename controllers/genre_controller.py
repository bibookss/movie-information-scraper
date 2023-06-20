from models import Genre
from peewee import IntegrityError

def add_genre(_name):
    try:
        genre = Genre.create(name=_name)
        return genre
    except IntegrityError as e:
        existing_genre = Genre.get(name=_name)
        print('Genre with the same name already exists.', str(e))
        return existing_genre

def get_genre(_name):
    try:
        genre = Genre.get(name=_name)
        return genre
    except Genre.DoesNotExist as e:
        print('Genre does not exist.', str(e))
        return add_genre(_name)

from models import Genre
from peewee import IntegrityError

def add_genre(_name):
    try:
        genre = Genre.create(name=_name)
        return genre
    except IntegrityError:
        existing_genre = Genre.get(name=_name)
        print('Genre with the same name already exists.')
        return existing_genre

def get_genre(_name):
    try:
        genre = Genre.get(name=_name)
        return genre
    except IntegrityError:
        print('Genre does not exist.')
        return add_genre(_name)

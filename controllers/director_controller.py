from models import Director
from peewee import IntegrityError

def add_director(_name):
    try:
        print(f'Adding director {_name}')
        director = Director.create(name=_name)
        return director
    except IntegrityError as e:
        existing_director = Director.get(name=_name)
        print('Director with the same name already exists.', str(e))
        return existing_director

def get_director(_name):
    try:
        director = Director.get(name=_name)
        return director
    except Director.DoesNotExist as e:
        print('Director not found.', str(e))
        return add_director(_name)


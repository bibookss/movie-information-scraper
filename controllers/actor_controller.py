from models import Actor
from peewee import IntegrityError

def add_actor(_name):
    try:
        print(f'Adding actor {_name}.')
        actor = Actor.create(name=_name)
        return actor
    except IntegrityError as e:
        existing_actor = Actor.get(name=_name)
        print('Actor with the same name already exists.', str(e))
        return existing_actor

def get_actor(_name):
    try:
        actor = Actor.get(name=_name)
        return actor
    except Actor.DoesNotExist as e:
        print('Actor does not exist.', str(e))
        return add_actor(_name)

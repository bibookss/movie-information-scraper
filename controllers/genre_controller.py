from models import Genre

def add_genre(_name):
    try:
        genre = Genre.create(name=_name)
        return genre
    except IntegrityError:
        existing_genre = Genre.get(name=_name)
        print('Genre with the same name already exists.')
        return existing_genre

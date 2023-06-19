from models import Movie
from peewee import IntegrityError

def add_movie(_name, _url):
    try:
        url = 'https://www.themoviedb.org' + _url
        movie = Movie.create(name=_name, url=_url) 
    except IntegrityError:
        print(f'Movie with the same url, {_url}, already exists.')
        
def set_movie_details(_url, _description, _certification, _release, _genres):
    try:
        release_date = datetime.datetime.strptime(_release, '%m/%d/%Y').date()
        loaded_genres = [add_genre(i) for i in _genres]
        Movie.update(           
            description=_description, 
            certification=_certification, 
            release=release_date, 
            genres=loaded_genres
        ).where(Movie.url == _url).execute()        
    except IntegrityError:
        print('Movie not found.')

def get_unvisited_movies():
    query = Movie.select().where(Movie.is_visited == False)
    return query

def set_movie_visited(_url):
    try:        
        movie = Movie.get(Movie.url == _url)
        movie.is_visited = True
        movie.save()
    except IntegrityError:
        print('Movie does not exist')

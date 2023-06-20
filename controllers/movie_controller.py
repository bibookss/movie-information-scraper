from models import Movie, db
from peewee import IntegrityError
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from controllers.genre_controller import get_genre

def add_movie(_name, _url):
    try:
        _url = 'https://www.themoviedb.org' + _url
        movie = Movie.create(name=_name, url=_url) 
    except IntegrityError:
        print(f'Movie with the same url, {_url}, already exists.')
        
def set_movie_details(_url, _details):
    try:
        movie = Movie.get(Movie.url == _url)

        if 'release' in _details:
            movie.release = _details['release']
        else:
            movie.release = None

        if 'overview' in _details:
            movie.description =_details['overview']
        else:
            movie.overview = None

        if 'certification' in _details:
            movie.certification = _details['certification']
        else:
            movie.certification = None

        if 'runtime' in _details:
            movie.duration = _details['runtime']
        else:
            movie.runtime = None

        if 'genres' in _details:
            genres = _details['genres']
            loaded_genres = [get_genre(i) for i in genres]
            try:
                movie.genres.add(loaded_genres)
            except:
                pass
        else:
            movie.genres.add([])

        movie.is_visited = True

        return movie

    except IntegrityError as e:
        print('Movie not found.', e)
        return None

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

def convert_duration_to_minutes(duration):    
    duration_l = duration.split()
    total_minutes = 0
    
    if 'h' in duration:
        h = int(duration_l[0].replace('h', ''))
        total_minutes += h * 60
        
    if 'm' in duration:
        if len(duration_l) == 2:
            m = int(duration_l[1].replace('m', ''))
        else:
            m = int(duration_l[0].replace('m', ''))

        total_minutes += m
    
    return total_minutes

def convert_date_to_datetime(date):
    date = date.split()[0]
    date_format = "%m/%d/%Y"

    date_object = datetime.strptime(date, date_format).date()

    return date_object
    
def convert_genres_to_list(genres):
    genres = genres.split(',')
    genres = [genre.replace('\xa0', '') for genre in genres]
    return genres

def scrape_movie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
    
    div_facts = soup.find('div', class_='facts')
    span_elements = div_facts.find_all('span')
    
    details = {}
    for span in span_elements:
        details[span.get('class')[0]] = span.text
        
    div_overview = soup.find('div', class_='overview')
    p = div_overview.find('p')
    
    details['overview'] = p.text
            
    return details

def clean_movie_details(details):
    cleaned_data = {key: value.strip().replace('\n', '').replace('\r', '').replace('\t', '') 
                    for key, value in details.items()}
    
    if 'release' in cleaned_data:
        cleaned_data['release'] = convert_date_to_datetime(cleaned_data['release'])
    
    if 'genres' in cleaned_data:
        cleaned_data['genres'] = convert_genres_to_list(cleaned_data['genres'])
        
    if 'runtime' in cleaned_data:
        cleaned_data['runtime'] = convert_duration_to_minutes(cleaned_data['runtime'])
    
    return cleaned_data

def bulk_update_movies(movies):
    try:
        _fields = [
            Movie.release,
            Movie.description,
            Movie.duration,
            Movie.certification,
            Movie.is_visited]

        with db.atomic():
            filtered_movies = [movie for movie in movies if movie is not None]
            Movie.bulk_update(filtered_movies, fields=_fields, batch_size=20)

    except Exception as e:
        db.rollback()
        print('Error occured during bulk update:', str(e))


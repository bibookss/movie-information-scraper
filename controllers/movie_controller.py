from models import Movie
from peewee import IntegrityError
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from controllers.genre_controller import add_genre

def add_movie(_name, _url):
    try:
        _url = 'https://www.themoviedb.org' + _url
        movie = Movie.create(name=_name, url=_url) 
    except IntegrityError:
        print(f'Movie with the same url, {_url}, already exists.')
        
def set_movie_details(_url, _description, _certification, _release, _genres, _duration):
    try:
        loaded_genres = [add_genre(i) for i in _genres]
        Movie.update(           
            description=_description, 
            certification=_certification, 
            release=_release, 
            duration=_duration
        ).where(Movie.url == _url).execute()   
        
        movie = Movie.get(Movie.url == _url)
        movie.genres.add(loaded_genres)

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

def convert_duration_to_minutes(duration):
    hours, minutes = duration.split('h')
    minutes = minutes.replace('m', '')

    total_minutes = int(hours) * 60 + int(minutes)
    
    return total_minutes

def convert_date_to_datetime(date):
    date = date.split()[0]
    date_format = "%m/%d/%Y"

    date_object = datetime.strptime(date, date_format).date()

    return date_object
    
def convert_genres_to_list(genres):
    return genres.split(',')

def scrape_movie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
    
    div_facts = soup.find('div', class_='facts')
    span_elements = div_facts.find_all('span')
    
    details = []
    for span in span_elements:
        details.append(span.text)
        
    div_overview = soup.find('div', class_='overview')
    p = div_overview.find('p')
    
    details.append(p.text)
            
    return clean_movie_details(details) 

def clean_movie_details(details):
    cleaned_data = [item.strip().replace('\n', '').replace('\xa0', '') for item in details]
    cleaned_data[1] = convert_date_to_datetime(cleaned_data[1])
    cleaned_data[2] = convert_genres_to_list(cleaned_data[2])
    cleaned_data[3] = convert_duration_to_minutes(cleaned_data[3])
    
    return cleaned_data
    

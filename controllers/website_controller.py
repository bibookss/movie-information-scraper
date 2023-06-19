from models import Website
import requests
from bs4 import BeautifulSoup as bs

def add_website(url):
    try:
        website = Website.create(url=url)
    except IntegrityError:
        print('Website with same url already exists.')

def get_unvisited_websites():
    query = Website.select().where(Website.is_visited == False)
    return query

def set_website_visited(url):
    try:        
        website = Website.get(Website.url == url)
        website.is_visited = True
        website.save()
    except IntegrityError:
        print('Website does not exist')

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
            
    div = soup.find('div', class_='page_wrapper')
    div2 = div.find_all('div', class_='content')

    titles = []
    for div_element in div2:
        a_tags = div_element.find_all('a')
        for a_tag in a_tags:
            movie = (a_tag['title'], a_tag['href'])
            titles.append(movie)
    
    return titles

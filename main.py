from controllers.movie_controller import * 
from controllers.website_controller import *
from controllers.genre_controller import *

def main():
    # Add pages to scrape
    website_url = 'https://www.themoviedb.org/movie?page='
    for i in range(1, 501):
        add_website(website_url + str(i))

    # Scrape each page
    unvisited_websites = get_unvisited_websites()

    for index, page in enumerate(unvisited_websites):
        movies = scrape_website(page.url)
        print(page.url) 
        for title, url in movies:
            add_movie(title, url)
        
        set_website_visited(page.url)
    
    # Scrape movie page
    unvisited_movies = get_unvisited_movies()
    movies = []
    for index, page in enumerate(unvisited_movies):
        print(page.url)
        details = scrape_movie(page.url)
        cleaned_details = clean_movie_details(details)
        
        movies.append(set_movie_details(page.url, cleaned_details))
        
        if index % 20 == 0:
            bulk_update_movies(movies)
            movies.clear()

if __name__ == '__main__':
    main()

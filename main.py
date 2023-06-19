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
    
        for title, url in movies:
            add_movie(title, url)
        
        set_website_visited(page.url)

if __name__ == '__main__':
    main()

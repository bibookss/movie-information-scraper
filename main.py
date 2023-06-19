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
    
    # Scrape movie page
    unvisited_movies = get_unvisited_movies()
    for index, page in enumerate(unvisited_movies):
        details = scrape_movie(page.url)
        set_movie_details(
                page.url,
                details[-1],
                details[0],
                details[1],
                details[2],
                details[3]) 

        set_movie_visited(page.url)
        if index == 20:
            break

if __name__ == '__main__':
    main()

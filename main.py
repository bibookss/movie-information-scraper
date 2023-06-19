from movie_controller import * 
from website_controller import *
from genre_controller import *

def main():
    website_url = 'https://www.themoviedb.org/movie?page='

    for i in range(1, 501):
        add_website(website_url + str(i))

if __name__ == '__main__':
    main()

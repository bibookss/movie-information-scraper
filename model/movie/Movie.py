class Movie:
    base_url: str = 'https://www.themoviedb.org/movie'
    def __init__(self, _title: str, _url: str) -> None:
        self.title = _title
        self.url = base_url + _url
    
    def set_description(self, _description: str) -> None:
        self.description = _description

    def set_information(self, _information: dict) -> None:
        self.certification = _information['certification']
        self.release = _information['release']
        self.genre = _information['genre']
        self.runtime = _information['runtime']
    
    def get_url(self) -> str:
        return self.url

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'certification': self.certification,
            'release': self.release,
            'genre': self.genre,
            'runtime': self.runtime,
            'url': self.url
        }

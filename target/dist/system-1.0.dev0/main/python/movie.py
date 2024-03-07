# movie.py
class Movie:
    def __init__(self, movie_id, name, director, release, language, subtitle, rate):
        self.id = movie_id
        self.name = name
        self.director = director
        self.release = release
        self.language = language
        self.subtitle = subtitle
        self.rate = rate

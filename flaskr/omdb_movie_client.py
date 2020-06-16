from datetime import datetime
from typing import List, Dict, Any, Optional

import requests

from flaskr.entity.movie_snapshot import MovieSnapshot, MovieSnapshotRating


class Movie:

    def __init__(self, json: Dict[str, Any]):
        self.__title = json["Title"]
        self.__director = json["Director"]
        self.__released_date = datetime.strptime(json["Released"], '%d %b %Y').date()
        self.__ratings = json["Ratings"]

    @property
    def title(self):
        return self.__title

    @property
    def director(self):
        return self.__director

    @property
    def released_date(self):
        return self.__released_date

    def rating_source_at(self, index: int):
        return self.__ratings[index]["Source"]

    def rating_value_at(self, index: int):
        return self.__ratings[index]["Value"]

    def to_movie_snapshot(self) -> MovieSnapshot:
        ratings = [MovieSnapshotRating(self.rating_value_at(index), self.rating_source_at(index))
                   for index, rating in enumerate(self.__ratings)
                   ]
        return MovieSnapshot(self.title, self.director, self.released_date, ratings)


class OmdbMovieClient:

    def __init__(self):
        from flaskr.flask_application import Application
        from flaskr.logger_factory import LoggerFactory
        self.api_key = Application.instance().configuration_value_for("OMDB_API_KEY")
        self.logger = LoggerFactory.instance().logger()

    def get_movies_for(self, titles: List[str]) -> List[Movie]:
        movies: List[Movie] = []
        for title in titles:
            movie: Optional[Movie] = self.__get_a_movie_for(title)
            if movie is not None:
                movies.append(movie)

        return movies

    def __get_a_movie_for(self, title: str) -> Optional[Movie]:
        self.logger.info(f"Fetching {title} from OMDB")
        try:
            response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}")
            return Movie(response.json())
        except requests.RequestException as ex:
            self.logger.error(f"Failed while fetching {title} with an exception {ex}")
            return None

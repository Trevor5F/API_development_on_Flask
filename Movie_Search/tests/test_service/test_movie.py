from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.model.genre import Genre
from dao.model.director import Director
from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1, title='Йеллоустоун', description='описание 1', trailer='ссылка', year=2000,
                    rating=9.1, genre_id=1, director_id=1)
    movie_2 = Movie(id=2, title='Омерзительная восьмерка', description='описание 2', trailer='ссылка', year=2010,
                    rating=9.1, genre_id=2, director_id=2)
    movie_3 = Movie(id=3, title='Вооружен и очень опасен', description='описание 3', trailer='ссылка', year=2020,
                    rating=9.1, genre_id=3, director_id=3)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=1))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie):
        self.movie_service = MovieService(dao=movie)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "id": 1,
            "title": "new_title",
            "description": "new_description",
            "trailer": "new_trailer",
            "year": 2001,
            "rating": 8.0,
            "genre_id": 3,
            "director_id": 3
        }
        movie = self.movie_service.create(movie_d)

        assert movie.id is not None

    def test_update(self):
        movie_d = {
            "id": 2,
            "title": "new_title2",
            "description": "new_description2",
            "trailer": "new_trailer2",
            "year": 2001,
            "rating": 8.0,
            "genre_id": 3,
            "director_id": 3
        }
        self.movie_service.update(movie_d)


    def test_delete(self):
        self.movie_service.delete(1)

from unittest.mock import MagicMock

import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre():
    genre_dao = GenreDAO(None)

    comedy = Genre(id=1, name='comedy')
    drama = Genre(id=2, name='drama')
    horror = Genre(id=3, name='horror')

    genre_dao.get_one = MagicMock(side_effect=lambda gid: comedy if gid == 1 else None)
    genre_dao.get_all = MagicMock(return_value=[comedy, drama, horror])
    genre_dao.create = MagicMock(return_value=Genre(id=1))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre):
        self.genre_service = GenreService(dao=genre)


    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None
        assert genre.name is not None
        # assert genre is None


    def test_get_all(self):
        genre = self.genre_service.get_all()

        assert len(genre) > 0

    def test_create(self):
        genre_d = {"name": "action"}
        genre = self.genre_service.create(genre_d)

        assert genre.id is not None

    def test_update(self):
        genre_d = {
            "id": 3,
            "name": "comedy"
        }
        self.genre_service.update(genre_d)


    def test_delete(self):
        self.genre_service.delete(1)

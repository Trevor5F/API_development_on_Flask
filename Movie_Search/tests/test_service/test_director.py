from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director():
    director_dao = DirectorDAO(None)

    jonh = Director(id=1, name='jonh')
    kate = Director(id=2, name='kate')
    max = Director(id=3, name='max')


    director_dao.get_one = MagicMock(return_value=jonh)
    director_dao.get_all = MagicMock(return_value=[jonh, kate, max])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.partially_update = MagicMock(return_value=Director(id=2))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director):
        self.director_service = DirectorService(dao=director)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director != None
        assert director.id != None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Ivan",
        }
        director = self.director_service.create(director_d)
        assert director.id != None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Ivan",
        }
        self.director_service.update(director_d)
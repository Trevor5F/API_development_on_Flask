from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, filters=None):
        if filters is None:
            filters = {}
        return self.dao.get_all(filters)

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        return self.dao.update(movie_d)

    def partial_update(self, movie_d):
        return self.dao.partial_update(movie_d)

    def delete(self, rid):
        self.dao.delete(rid)

import sqlite3

def db_connect(query):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def search_by_title(title):
    query = """
            SELECT title, country, release_year, listed_in AS genre, description
            FROM netflix
            WHERE title LIKE '%{}%'
            ORDER BY release_year DESC
            LIMIT 1
    """.format(title)
    result = db_connect(query)
    if result:
        data = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4].strip()
        }
        return data
    else:
        return 'По заданному названию результатов не найдено.'


def movie_year(start: int, end: int):
    query = """
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {} AND {}
            ORDER BY release_year
            LIMIT 100
    """.format(start, end)
    results = db_connect(query)
    return [{"title": result[0], "release_year": result[1]} for result in results]


def by_ratings(rating):
    query = """
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({})
            ORDER BY rating
            LIMIT 10
            """.format(", ".join(f"'{r}'" for r in rating))
    results = db_connect(query)
    return [{"title": movie[0], "rating": movie[1], "description": movie[2].strip()} for movie in results]


def movie_genre(genre):
    query = """
            SELECT title, listed_in AS genre, description
            FROM netflix
            WHERE listed_in = '{}'
            LIMIT 10
    """.format(genre)
    results = db_connect(query)
    return [{"title": movie[0], "genre": movie[1], "description": movie[2].strip()} for movie in results]


def movie_cast(name1='Rose McIver', name2='Ben Lamb'):
    query = """
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{}%' AND "cast" LIKE '%{}%'
    """.format(name1, name2)
    results = db_connect(query)

    actor_counts = {}
    for result in results:
        cast = result[0].split(', ')
        for actor in cast:
            actor_counts[actor.strip()] = actor_counts.get(actor.strip(), 0) + 1
    return [actor for actor, count in actor_counts.items() if count > 2 and actor not in [name1, name2]]
print(movie_cast())


def get_films(type_film='Movie', release_year=2016, genre='Dramas'):
    query = """
            SELECT title, description, "type"
            FROM netflix
            WHERE "type" = '{}'
            AND release_year = {}
            AND listed_in LIKE '%{}%'
    """.format(type_film, release_year, genre)
    results = db_connect(query)
    return [{"title": movie[0], "description": movie[1].strip(), "genre": movie[2]} for movie in results]

from collections import deque
from multiprocessing import Pool, Manager
from .web import get_json_data
from .person import Person


def fetch_data(url):
    """Fetch data for a single URL."""
    return url, get_json_data(url)


def find_degrees_of_separation(person1_url, person2_url):
    # Initialize data structures
    manager = Manager()
    visited_actors = manager.dict()
    visited_movies = manager.dict()
    enqueued_actors = manager.dict()
    que = deque()

    person_zero = Person(url=person1_url, degree=0)
    que.append(person_zero)

    # Start BFS (Breadth First Search)
    with Pool(processes=4) as pool:
        while que:
            current_person = que.popleft()
            if current_person.url == person2_url:
                current_person.show_result()
                return current_person.degree

            # Check if visited
            if visited_actors.get(current_person.url, False):
                continue
            visited_actors[current_person.url] = True

            # Fetch all movies of this actor
            current_person_data = pool.apply_async(get_json_data, [current_person.url]).get(timeout=100)
            if current_person_data is None:
                continue

            current_person.name = current_person_data['name']
            movies = current_person_data['movies']
            cast_members = []

            # Prepare movie URL fetches
            movie_fetches = []
            for movie in movies:
                if movie and not visited_movies.get(movie['url'], False):
                    movie_fetches += [(movie['url'],movie)]
                    
            for movie_url, movie in movie_fetches:
                visited_movies[movie_url] = True

            # Fetch movie data
            results = pool.map(fetch_data, [movie_url for movie_url, _ in movie_fetches])
            for movie_url, movie_data in results:
                if movie_data is None:
                    continue
                cast_members.append(
                    (movie_data['name'], movie['role'], movie_url, movie_data['cast'] + movie_data['crew']))

            for movie_name, movie_role, movie_url, cast in cast_members:
                for connected_person in cast:
                    actor_url = connected_person['url']
                    if visited_actors.get(actor_url, False) or enqueued_actors.get(actor_url, False):
                        continue

                    actor = Person(
                        url=actor_url,
                        name=None,
                        movie_url=movie_url,
                        movie_name=movie_name,
                        role=connected_person['role'],
                        parent_person=current_person,
                        degree=current_person.degree + 1
                    )

                    if actor.url == person2_url:
                        actor.show_result()
                        return actor.degree

                    que.append(actor)
                    enqueued_actors[actor_url] = True

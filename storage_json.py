from istorage import IStorage
import json
import requests
from urllib.parse import quote_plus

class StorageJson(IStorage):
    """
    Storage class using JSON with API integration to fetch movie details.
    """
    API_KEY = "5429604c"  # 🔑 OMDb API key
    API_URL = "http://www.omdbapi.com/?apikey={}&t={}"  # API endpoint

    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file).get("movies", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as file:
            json.dump({"movies": movies}, file, indent=4)

    def fetch_movie_data(self, title):
        """Fetch movie details from OMDb API."""
        response = requests.get(self.API_URL.format(self.API_KEY, title.replace(" ", "+")))
        data = response.json()

        if data.get("Response") == "True":
            return {
                "year": int(data.get("Year", 0)),
                "rating": float(data.get("imdbRating", 0.0)),
                "poster": data.get("Poster", "https://via.placeholder.com/150"),
                "link": f"https://www.imdb.com/title/{data.get('imdbID', '')}"
            }
        else:
            print(f"❌ Movie '{title}' not found in OMDb API.")
            return None

    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the storage."""
        movies = self.list_movies()

        # Ensure the movie is not added twice accidentally
        if title in movies:
            print(f"⚠️ '{title}' is already in the collection.")
            return

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,
            "link": f"https://www.imdb.com/find?q={quote_plus(title)}"
        }

        self._save_movies(movies)  # Ensure this is called only once
        print(f"✅ '{title}' added successfully!")

    def delete_movie(self, title):
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def list_movies(self):
        """Return all movies as a dictionary."""
        return self._load_movies()

    def display_movies(self):
        """Display all movies in a nice format."""
        movies = self._load_movies()
        if not movies:
            print("\n🎬 Your Movie Collection is empty 🎬")
        else:
            print("\n🎬 Your Movie Collection 🎬")
            print("=" * 50)
            for title, movie in movies.items():
                print(f"📽️ Title: {title}")
                print(f"📆 Year: {movie['year']}")
                print(f"⭐ Rating: {movie['rating']}/10")
                print(f"🖼️ Poster: {movie['poster']}")
                print(f"🔗 More Info: {movie['link']}")
                print("-" * 50)


# ✅ **Testing API Integration**
if __name__ == "__main__":
    storage = StorageJson("movies.json")
    storage.add_movie("Malcolm & Marie")  # 🎬 Fetches data from OMDb API!
    storage.display_movies()
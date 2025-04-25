from .istorage import IStorage  # ✅ Uses relative import
import os
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
        """Load movies from JSON file correctly."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if "movies" in data:  # ✅ Fix: Extract movies correctly
                        return data["movies"]
                    return data
            else:
                print("⚠️ No movies.json file found, starting with an empty collection.")
                return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error loading JSON file: {e}")
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

        if title in movies:
            return False

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,
            "link": f"https://www.imdb.com/find?q={quote_plus(title)}"
        }

        self._save_movies(movies)
        return True

    def update_movie(self, title, rating):
        """Update a movie's rating in the storage."""
        movies = self._load_movies()
        title_mapping = {k.lower(): k for k in movies.keys()}

        if title.lower() in title_mapping:
            actual_title = title_mapping[title.lower()]
            movies[actual_title]['rating'] = rating
            self._save_movies(movies)
            return True
        return False

    def delete_movie(self, title):
        """Delete a movie from the storage."""
        movies = self._load_movies()
        title_mapping = {k.lower(): k for k in movies.keys()}

        if title.lower() in title_mapping:
            actual_title = title_mapping[title.lower()]
            del movies[actual_title]
            self._save_movies(movies)
            return True
        return False

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
    storage = StorageJson("../data/movies.json")
    storage.add_movie("Malcolm & Marie")  # 🎬 Fetches data from OMDb API!
    storage.display_movies()
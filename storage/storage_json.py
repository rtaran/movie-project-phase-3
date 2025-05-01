from .istorage import IStorage  # ✅ Uses relative import
import os
import json
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StorageJson(IStorage):
    """
    Storage class using JSON with API integration to fetch movie details.
    """
    API_URL = "http://www.omdbapi.com/?apikey={}&t={}"  # API endpoint

    def __init__(self, file_path):
        self.file_path = file_path
        # Get API key from environment variable
        self.api_key = os.getenv("OMDB_API_KEY", "")
        if not self.api_key:
            print("⚠️ Warning: OMDB_API_KEY environment variable not set.")

    def _load_movies(self):
        """
        Load movies from JSON file correctly.

        Returns:
            dict: Dictionary of movie information
        """
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
        """
        Save movies to JSON file.

        Args:
            movies (dict): Dictionary of movie information to save
        """
        with open(self.file_path, 'w', encoding="utf-8") as file:
            json.dump({"movies": movies}, file, indent=4)

    def fetch_movie_data(self, title):
        """
        Fetch movie details from OMDb API.

        Args:
            title (str): The title of the movie to fetch

        Returns:
            dict: Movie details if found, None otherwise
        """
        try:
            response = requests.get(
                self.API_URL.format(self.api_key, title.replace(" ", "+")),
                timeout=10  # Add timeout to prevent hanging indefinitely
            )
            response.raise_for_status()  # Raise exception for HTTP errors
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
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out while fetching data for '{title}'.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching movie data: {e}")
            return None

    def add_movie(self, title, year=None, rating=None, poster=None):
        """
        Adds a movie to the storage. If only title is provided, attempts to fetch other details.

        Args:
            title (str): The title of the movie
            year (str, optional): The release year of the movie
            rating (float, optional): The rating of the movie (1-10)
            poster (str, optional): URL to the movie poster image

        Returns:
            bool: True if movie was added successfully, False otherwise
        """
        # If only title is provided, try to fetch movie data
        if year is None and rating is None and poster is None and self.api_key:
            movie_data = self.fetch_movie_data(title)
            if movie_data:
                year = movie_data["year"]
                rating = movie_data["rating"]
                poster = movie_data["poster"]

                # Call the parent class implementation with the fetched data
                movies = self._load_movies()

                if title in movies:
                    return False

                movies[title] = {
                    "year": year,
                    "rating": rating,
                    "poster": poster,
                    "link": movie_data["link"]
                }

                self._save_movies(movies)
                return True
            return False

        # If all details are provided, use parent class implementation
        movies = self._load_movies()

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

    def display_movies(self):
        """
        Display all movies in a nice format.
        """
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

import csv
import requests
import os
from dotenv import load_dotenv
from istorage import IStorage

# Load environment variables
load_dotenv()

class StorageCsv(IStorage):
    """
    Storage class using CSV with API integration to fetch movie details.
    """
    API_KEY = os.getenv("OMDB_API_KEY")  # Load API key from .env file
    API_URL = "http://www.omdbapi.com/?apikey={}&t={}"  # API endpoint

    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """Load movies from CSV file and return as dictionary."""
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row['title']] = {
                        "year": int(row['year']),
                        "rating": float(row['rating']),
                        "poster": row.get('poster', f"https://www.imdb.com/find?q={row['title'].replace(' ', '+')}"),
                        "link": row.get('link', f"https://www.imdb.com/find?q={row['title'].replace(' ', '+')}")
                    }
        except FileNotFoundError:
            pass
        return movies

    def _save_movies(self, movies):
        """Save movies dictionary to CSV file."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'year', 'rating', 'poster', 'link']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "year": details['year'],
                    "rating": details['rating'],
                    "poster": details['poster'],
                    "link": details['link']
                })

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

    def add_movie(self, title):
        """Automatically fetch and add movie details."""
        movies = self._load_movies()
        if title in movies:
            print(f"⚠️ '{title}' already exists in the collection.")
            return

        movie_data = self.fetch_movie_data(title)
        if movie_data:
            movies[title] = movie_data
            self._save_movies(movies)
            print(f"✅ '{title}' added successfully!")
        else:
            print(f"❌ Unable to add '{title}'.")

    def delete_movie(self, title):
        """Delete a movie from storage."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """Update a movie's rating."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def list_movies(self):
        """Return all movies as a dictionary."""
        return self._load_movies()

    def display_movies(self):
        """Display all movies in a formatted style."""
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
    storage = StorageCsv("movies.csv")
    storage.add_movie("Parthenope")  # 🎬 Fetches data from OMDb API!
    storage.display_movies()

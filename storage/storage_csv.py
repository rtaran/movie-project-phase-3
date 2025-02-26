import csv
import os
from .istorage import IStorage

class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """Load movies from CSV file."""
        movies = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row["title"]] = {
                        "year": row["year"],
                        "rating": float(row["rating"]),
                        "poster": row["poster"]
                    }
        return movies

    def _save_movies(self, movies):
        """Save movies to CSV file."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({"title": title, "year": details["year"], "rating": details["rating"], "poster": details["poster"]})

    def list_movies(self):
        """Return all movies as a dictionary."""
        return self._load_movies()

    def add_movie(self, title, year, rating, poster):
        """Add a movie to the CSV file."""
        movies = self._load_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self._save_movies(movies)
        print(f"✅ '{title}' added successfully!")

    def delete_movie(self, title):
        """Delete a movie from the CSV file."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"🗑️ '{title}' removed successfully!")
        else:
            print(f"❌ Error: Movie '{title}' not found!")

    def update_movie(self, title, rating):
        """Update a movie's rating in the CSV file."""
        movies = self._load_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)
            print(f"✏️ '{title}' rating updated successfully!")
        else:
            print(f"❌ Error: Movie '{title}' not found!")
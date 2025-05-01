import csv
import os
from .istorage import IStorage
from urllib.parse import quote_plus

class StorageCsv(IStorage):
    """
    Storage class using CSV file format.
    """
    def __init__(self, file_path):
        """
        Initialize the CSV storage.

        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = file_path

    def _load_movies(self):
        """
        Load movies from CSV file.

        Returns:
            dict: Dictionary of movie information
        """
        movies = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row["title"]] = {
                        "year": row["year"],
                        "rating": float(row["rating"]),
                        "poster": row["poster"],
                        "link": (f"https://www.imdb.com/find?q="
                                f"{quote_plus(row['title'])}")  # Add default link
                    }
        return movies

    def _save_movies(self, movies):
        """
        Save movies to CSV file.

        Args:
            movies (dict): Dictionary of movie information to save
        """
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "year": details["year"], 
                    "rating": details["rating"],
                    "poster": details["poster"]
                })

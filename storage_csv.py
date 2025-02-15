import csv
from istorage import IStorage


class StorageCsv(IStorage):
    """
    Implementation of IStorage using CSV for persistent storage.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """Load movies from the CSV file and return them as a dictionary."""
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row['title']] = {
                        "rating": float(row['rating']),
                        "year": int(row['year']),
                        "poster": row.get('poster', f"https://www.imdb.com/find?q={row['title'].replace(' ', '+')}"),
                        "link": row.get('link', f"https://www.imdb.com/find?q={row['title'].replace(' ', '+')}")
                    }
        except FileNotFoundError:
            pass
        return movies

    def _save_movies(self, movies):
        """Save the movies dictionary into the CSV file."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'rating', 'year', 'poster', 'link']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "rating": details['rating'],
                    "year": details['year'],
                    "poster": details['poster'],
                    "link": details['link']
                })

    def list_movies(self):
        """Return all movies as a dictionary."""
        return self._load_movies()

    def add_movie(self, title, year, rating, poster=None, link=None):
        """Add a movie to the storage."""
        movies = self._load_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster or f"https://www.imdb.com/find?q={title.replace(' ', '+')}",
            "link": link or f"https://www.imdb.com/find?q={title.replace(' ', '+')}"
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        """Delete a movie from the storage."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """Update the rating of a movie in the storage."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def display_movies(self):
        """Display all movies in a nice format."""
        movies = self._load_movies()
        if not movies:
            print("\n🎬 Your Movie Collection is empty 🎬")
            return
        if any(movies):  # Ensures it's printed only once
            print("\n🎬 Your Movie Collection 🎬")
            print("=" * 50)
            for title, movie in movies.items():
                print(f"📽️ Title: {title}")
                print(f"📆 Year: {movie['year']}")
                print(f"⭐ Rating: {movie['rating']}/10")
                print(f"🖼️ Poster: {movie['poster']}")
                print(f"🔗 More Info: {movie['link']}")
                print("-" * 50)


# Testing the StorageCsv class
if __name__ == "__main__":
    storage = StorageCsv("movies.csv")
    storage.add_movie("Titanic", 1997, 9.2, "https://www.imdb.com/title/tt0120338/mediaviewer/rm2647458304")
    storage.update_movie("Titanic", 9.5)
    storage.display_movies()
    storage.delete_movie("Titanic")
    storage.display_movies()

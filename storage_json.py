from istorage import IStorage
import json

class StorageJson(IStorage):
    """
    Implementation of IStorage using JSON for persistent storage.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file).get("movies", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as file:
            json.dump({"movies": movies}, file, indent=4)

    def list_movies(self):
        return self._load_movies()

    def add_movie(self, title, year, rating, poster=None, link=None):
        movies = self._load_movies()
        movies.append({
            "title": title,
            "year": year,
            "rating": rating,
            "poster": poster or f"https://www.imdb.com/title/tt0120338/mediaviewer/rm2647458304/?ref_=tt_ov_i{title.replace(' ', '_').lower()}.jpg",
            "link": link or f"https://www.imdb.com/find?q={title.replace(' ', '+')}"
        })
        self._save_movies(movies)

    def delete_movie(self, title):
        movies = self._load_movies()
        movies = [movie for movie in movies if movie["title"] != title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        movies = self._load_movies()
        for movie in movies:
            if movie["title"] == title:
                movie["rating"] = rating
        self._save_movies(movies)

    def display_movies(self):
        movies = self._load_movies()
        print("\n🎬 Your Movie Collection 🎬")
        print("=" * 50)
        for movie in movies:
            print(f"📽️ Title: {movie['title']}")
            print(f"📆 Year: {movie['year']}")
            print(f"⭐ Rating: {movie['rating']}/10")
            print(f"🖼️ Poster: {movie['poster']}")
            print(f"🔗 More Info: {movie['link']}")
            print("-" * 50)

# Testing the StorageJson class
if __name__ == "__main__":
    storage = StorageJson("movies.json")
    storage.add_movie("Titanic", 1997, 9)
    storage.update_movie("Titanic", 10)
    storage.display_movies()
    storage.delete_movie("Titanic")
    storage.display_movies()

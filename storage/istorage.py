from abc import ABC, abstractmethod

class IStorage(ABC):
    """Interface for movie storage implementations."""

    @abstractmethod
    def _load_movies(self):
        """
        Load movies from storage.

        This method should be implemented by subclasses to load movies from their specific storage format.

        Returns:
            dict: Dictionary of movie information
        """
        pass

    @abstractmethod
    def _save_movies(self, movies):
        """
        Save movies to storage.

        This method should be implemented by subclasses to save movies to their specific storage format.

        Args:
            movies (dict): Dictionary of movie information to save
        """
        pass

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function returns a dictionary of dictionaries where each key is a movie title
        and the value is a dictionary with the movie's information (year, rating, poster, link).

        Returns:
            dict: Dictionary of movie information
        """
        return self._load_movies()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movie database.

        Args:
            title (str): The title of the movie
            year (str): The release year of the movie
            rating (float): The rating of the movie (1-10)
            poster (str): URL to the movie poster image

        Returns:
            bool: True if movie was added successfully, False otherwise
        """
        movies = self._load_movies()

        if title in movies:
            return False

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }

        self._save_movies(movies)
        return True

    def delete_movie(self, title):
        """
        Deletes a movie from the movie database.

        Args:
            title (str): The title of the movie to delete

        Returns:
            bool: True if movie was deleted successfully, False otherwise
        """
        movies = self._load_movies()
        title_mapping = {k.lower(): k for k in movies.keys()}

        if title.lower() in title_mapping:
            actual_title = title_mapping[title.lower()]
            del movies[actual_title]
            self._save_movies(movies)
            return True
        return False

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the movie database.

        Args:
            title (str): The title of the movie
            rating (float): The new rating for the movie

        Returns:
            bool: True if movie was updated successfully, False otherwise
        """
        movies = self._load_movies()
        title_mapping = {k.lower(): k for k in movies.keys()}

        if title.lower() in title_mapping:
            actual_title = title_mapping[title.lower()]
            movies[actual_title]['rating'] = rating
            self._save_movies(movies)
            return True
        return False

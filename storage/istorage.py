from abc import ABC, abstractmethod

class IStorage(ABC):
    """Interface for movie storage implementations."""

    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function returns a dictionary of dictionaries where each key is a movie title
        and the value is a dictionary with the movie's information (year, rating, poster, link).

        Returns:
            dict: Dictionary of movie information
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movie database.

        Args:
            title (str): The title of the movie
            year (str): The release year of the movie
            rating (float): The rating of the movie (1-10)
            poster (str): URL to the movie poster image
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the movie database.

        Args:
            title (str): The title of the movie to delete
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the movie database.

        Args:
            title (str): The title of the movie
            rating (float): The new rating for the movie
        """
        pass
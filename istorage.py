from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Interface for storage classes. Defines the standard operations for managing movie data.
    """
    @abstractmethod
    def list_movies(self):
        """Returns a dictionary containing all stored movies."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Adds a new movie to the storage."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Removes a movie from the storage by title."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Updates the rating of an existing movie."""
        pass

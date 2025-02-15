import json
import os

DATA_FILE = "data.json"

def load_movies():
    """Loads movie data from a JSON file. Ensures it extracts the list under 'movies'."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            # Ensure 'movies' exists and is a list
            if isinstance(data, dict) and "movies" in data and isinstance(data["movies"], list):
                return data["movies"]  # Extract movie list

            print("Error: JSON structure is incorrect. Expected {'movies': [...]}")
            return []  # Reset if format is wrong

    except json.JSONDecodeError:
        print("Error: Could not read JSON data. Resetting to an empty database.")
        return []

def save_movies(movies):
    """Saves the current movie data into a JSON file inside 'movies' key."""
    data = {"movies": movies}  # ✅ Ensure data is stored correctly
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_movie(title, rating, year):
    """Adds a new movie with a title, rating, and year to JSON storage."""
    movies = load_movies()

    for movie in movies:
        if movie["title"] == title:
            print(f"Error: Movie '{title}' already exists.")
            return

    new_movie = {"title": title, "rating": rating, "year": year}
    movies.append(new_movie)  # ✅ Append correctly
    save_movies(movies)
    print(f"Movie '{title}' ({year}) added successfully.")


def delete_movie(title):
    """Deletes a movie from the JSON storage."""
    movies = load_movies()

    # Standardize title format for comparison
    title = title.strip().lower()

    updated_movies = [movie for movie in movies if movie["title"].lower() != title]  # 🔹 Compare lowercase

    if len(updated_movies) == len(movies):
        print(f"Error: Movie '{title}' not found.")  # 🔹 Movie was not deleted
    else:
        save_movies(updated_movies)
        print(f"Movie '{title}' deleted successfully.")


def update_movie(title, new_rating):
    """Updates the rating of an existing movie."""
    movies = load_movies()

    # Standardize title format for comparison
    title = title.strip().lower()

    for movie in movies:
        if movie["title"].lower() == title:  # 🔹 Compare lowercase
            movie["rating"] = new_rating  # Update rating
            save_movies(movies)
            print(f"Movie '{movie['title']}' updated to rating {new_rating}.")
            return

    print(f"Error: Movie '{title}' not found.")  # 🔹 Case-sensitive check is now fixed

def list_movies():
    """Lists all movies stored in the JSON file."""
    movies = load_movies()

    if not movies:
        print("No movies found.")
        return

    print(f"{len(movies)} movies in total:")
    for movie in movies:
        if isinstance(movie, dict):  # Ensure movie is a dictionary
            title = movie.get("title", "Unknown Title")
            rating = movie.get("rating", "N/A")
            year = movie.get("year", "Unknown Year")
            print(f"{title} ({year}): ⭐ {rating}")
        else:
            print(f"Warning: Unexpected data format -> {movie}")

    print(f"{len(movies)} movies in total:")
    for movie in movies:
        if isinstance(movie, dict):  # Ensure movie is a dictionary
            title = movie.get("title", "Unknown Title")
            rating = movie.get("rating", "N/A")
            year = movie.get("year", "Unknown Year")
            print(f"{title} ({year}): ⭐ {rating}")
        else:
            print(f"Warning: Unexpected data format -> {movie}")



# def get_movies():
#     """
#     Returns a dictionary of dictionaries that
#     contains the movies information in the database.
#
#     The function loads the information from the JSON
#     file and returns the data.
#
#     For example, the function may return:
#     {
#       "Titanic": {
#         "rating": 9,
#         "year": 1999
#       },
#       "..." {
#         ...
#       },
#     }
#     """
#     pass
#
# def save_movies(movies):
#     """
#     Gets all your movies as an argument and saves them to the JSON file.
#     """
#     pass
#
#
# def add_movie(title, year, rating):
#     """
#     Adds a movie to the movies database.
#     Loads the information from the JSON file, add the movie,
#     and saves it. The function doesn't need to validate the input.
#     """
#     pass
#
#
# def delete_movie(title):
#     """
#     Deletes a movie from the movies database.
#     Loads the information from the JSON file, deletes the movie,
#     and saves it. The function doesn't need to validate the input.
#     """
#     pass
#
#
# def update_movie(title, rating):
#     """
#     Updates a movie from the movies database.
#     Loads the information from the JSON file, updates the movie,
#     and saves it. The function doesn't need to validate the input.
#     """
#     pass
#
#___Advanced_Implementation_2
# Bonus Step
# This is a bonus step, you can skip it if you want.
# Objective
# The objective of this task is to create a Python function called filter_movies that allows users to filter a list of movies based on specific criteria such as minimum rating, start year, and end year.
# Requirements
# The function should prompt the user to input the minimum rating, start year, and end year.
# If the user leaves any input blank, it should be considered as no minimum rating, start year, or end year, respectively.
# It should filter the list of movies based on the provided criteria.
# The filtered movies should be displayed with their titles, release years, and ratings.
# Expected Output
# Enter minimum rating (leave blank for no minimum rating): 8.0
# Enter start year (leave blank for no start year): 2000
# Enter end year (leave blank for no end year):
# Filtered Movies:
# Movie 1 (2002): 8.1
# Movie 2 (2005): 8.5
# Decimals
# The current average and median ratings may display several decimal places, which can appear inconsistent with other scores typically shown with only one decimal place. To enhance user experience, consider limiting the display to just one or two decimal places. Instead of this:
# Average rating: 6.883333333333333
# Median rating: 7.95
# Best movie: In the Name of the Father, 8.1
# Worst movie: Bee Movie, 5.0
# The goal would be this:
# Average rating: 6.8
# Median rating: 7.9
# Best movie: In the Name of the Father, 8.1
# Worst movie: Bee Movie, 5.0
# Specification
# Optimize user experience by limiting the display of decimal places to one or two for average and median ratings.
# Hint:
# Utilize online resources such as Google or Stack Overflow for guidance.
# Before submitting the assignment, go back to the previous pages and make sure you fulfilled all of requirements.
# We highly recommend trying your code in different cases, to make sure it’s working properly.
# Good luck!

#___Advanced_Implementation
import json
import random
import statistics
import matplotlib.pyplot as plt  # For histogram
from fuzzywuzzy import fuzz, process  # For fuzzy search
from colorama import Fore, Style, init  # For colors

# Initialize colorama for Windows compatibility
init(autoreset=True)

DATA_FILE = "movies.json"

# Function to load movies from JSON
def load_movies():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data.get("movies", [])  # Extract list of movies
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file doesn't exist or is corrupted

# Function to save movies to JSON
def save_movies(movies):
    with open(DATA_FILE, "w") as file:
        json.dump({"movies": movies}, file, indent=4)

# Function to list all movies
def list_movies():
    movies = load_movies()
    if not movies:
        print(f"{Fore.RED}No movies found!{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}{len(movies)} movies in total:{Style.RESET_ALL}")
    for movie in movies:
        print(f"{Fore.GREEN}{movie['title']} ({movie['year']}): ⭐ {movie['rating']}{Style.RESET_ALL}")

# Function to add a movie
def add_movie():
    movies = load_movies()

    title = input(f"{Fore.YELLOW}Enter movie name: {Style.RESET_ALL}").strip()
    if any(movie["title"].lower() == title.lower() for movie in movies):
        print(f"{Fore.RED}Movie already exists!{Style.RESET_ALL}")
        return

    rating = input(f"{Fore.YELLOW}Enter rating (1-10): {Style.RESET_ALL}").strip()
    year = input(f"{Fore.YELLOW}Enter release year: {Style.RESET_ALL}").strip()

    if not (rating.replace(".", "").isdigit() and 1 <= float(rating) <= 10):
        print(f"{Fore.RED}Invalid rating! Please enter a number between 1 and 10.{Style.RESET_ALL}")
        return
    if not (year.isdigit() and 1888 <= int(year) <= 2025):
        print(f"{Fore.RED}Invalid year! Enter a valid movie release year (1888-2025).{Style.RESET_ALL}")
        return

    movies.append({"title": title, "rating": float(rating), "year": int(year)})
    save_movies(movies)
    print(f"{Fore.GREEN}Movie '{title}' ({year}) added successfully.{Style.RESET_ALL}")

# Function to delete a movie
def delete_movie():
    movies = load_movies()
    title = input(f"{Fore.YELLOW}Enter movie name to delete: {Style.RESET_ALL}").strip().lower()

    updated_movies = [movie for movie in movies if movie["title"].lower() != title]

    if len(updated_movies) == len(movies):
        print(f"{Fore.RED}Error: Movie '{title}' not found.{Style.RESET_ALL}")
    else:
        save_movies(updated_movies)
        print(f"{Fore.GREEN}Movie '{title}' deleted successfully.{Style.RESET_ALL}")

# Function to update a movie's rating
def update_movie():
    movies = load_movies()
    title = input(f"{Fore.YELLOW}Enter movie name to update: {Style.RESET_ALL}").strip().lower()

    for movie in movies:
        if movie["title"].lower() == title:
            rating = input(f"{Fore.YELLOW}Enter new rating (1-10): {Style.RESET_ALL}").strip()
            if not (rating.replace(".", "").isdigit() and 1 <= float(rating) <= 10):
                print(f"{Fore.RED}Invalid rating! Please enter a number between 1 and 10.{Style.RESET_ALL}")
                return

            movie["rating"] = float(rating)
            save_movies(movies)
            print(f"{Fore.GREEN}Updated '{movie['title']}' to new rating {rating}.{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}Error: Movie '{title}' not found.{Style.RESET_ALL}")

# Function to search movies using fuzzy matching
def search_movie():
    movies = load_movies()
    search_term = input(f"{Fore.YELLOW}Enter part of movie name: {Style.RESET_ALL}").strip().lower()

    found_movies = [movie for movie in movies if search_term in movie["title"].lower()]
    if found_movies:
        for movie in found_movies:
            print(f"{Fore.GREEN}{movie['title']} ({movie['year']}): ⭐ {movie['rating']}{Style.RESET_ALL}")
    else:
        similar_movies = process.extract(search_term, [movie["title"] for movie in movies], scorer=fuzz.ratio, limit=3)
        threshold = 60
        best_matches = [movie for movie, score in similar_movies if score >= threshold]

        if best_matches:
            print(f'{Fore.RED}Movie "{search_term}" not found. Did you mean:{Style.RESET_ALL}')
            for movie in best_matches:
                print(f"{Fore.YELLOW}- {movie}{Style.RESET_ALL}")
        else:
            print(f'{Fore.RED}No similar movies found for "{search_term}".{Style.RESET_ALL}')

# Function to sort movies by rating
def sort_movies():
    movies = load_movies()
    sorted_movies = sorted(movies, key=lambda x: x["rating"], reverse=True)
    for movie in sorted_movies:
        print(f"{Fore.GREEN}{movie['title']} ({movie['year']}): ⭐ {movie['rating']}{Style.RESET_ALL}")

# Function to create a histogram of ratings
def create_histogram():
    movies = load_movies()
    if not movies:
        print(f"{Fore.RED}No movies in database to create a histogram!{Style.RESET_ALL}")
        return

    ratings = [movie["rating"] for movie in movies]

    plt.figure(figsize=(8, 6))
    plt.hist(ratings, bins=5, edgecolor="black", alpha=0.7)
    plt.xlabel("Rating Ranges")
    plt.ylabel("Number of Movies")
    plt.title("Movie Ratings Histogram")

    filename = input(f"{Fore.YELLOW}Enter filename to save histogram (e.g., histogram.png): {Style.RESET_ALL}").strip()
    plt.savefig(filename)
    print(f"{Fore.GREEN}Histogram saved as {filename}!{Style.RESET_ALL}")

# Function to display menu
def menu():
    print(f"\n{Fore.BLUE}********** My Movies Database **********{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Menu:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}0. Exit{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1. List movies{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Add movie{Style.RESET_ALL}")
    print(f"{Fore.BLUE}3. Delete movie{Style.RESET_ALL}")
    print(f"{Fore.BLUE}4. Update movie{Style.RESET_ALL}")
    print(f"{Fore.BLUE}5. Search movie{Style.RESET_ALL}")
    print(f"{Fore.BLUE}6. Movies sorted by rating{Style.RESET_ALL}")
    print(f"{Fore.BLUE}7. Create Rating Histogram{Style.RESET_ALL}")


# Main function to handle user input
def main():
    while True:
        menu()
        choice = input(f"{Fore.YELLOW}Enter choice (0-7): {Style.RESET_ALL}").strip()

        if choice == "0":
            print(f"{Fore.GREEN}Exiting program. Goodbye! 🎬{Style.RESET_ALL}")
            break
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            search_movie()
        elif choice == "6":
            sort_movies()
        elif choice == "7":
            create_histogram()


if __name__ == "__main__":
    main()






#___Core_Implementation
"""
import movie_storage

def main():
    #Main menu for movie database management.#
    while True:
        print("\n********** My Movies Database **********")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")


        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            movie_storage.list_movies()
        elif choice == "2":
            title = input("Enter movie name: ").strip()
            rating = input("Enter rating (1-10): ").strip()
            year = input("Enter release year: ").strip()  # 🔹 Ask for year

            if rating.isdigit() and 1 <= int(rating) <= 10 and year.isdigit():
                movie_storage.add_movie(title, int(rating), int(year))  # ✅ Pass the year
            else:
                print("Invalid input. Rating must be between 1-10, and year must be a number.")
        elif choice == "3":
            title = input("Enter movie name to delete: ").strip()
            movie_storage.delete_movie(title)
        elif choice == "4":
            title = input("Enter movie name to update: ").strip()
            new_rating = input("Enter new rating (1-10): ").strip()
            if new_rating.isdigit() and 1 <= int(new_rating) <= 10:
                movie_storage.update_movie(title, int(new_rating))
            else:
                print("Invalid rating. Please enter a number between 1 and 10.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()"""
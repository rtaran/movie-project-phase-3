import requests
import random
import os
import statistics
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


class MovieApp:
    """
    The MovieApp class handles user interaction and commands to manage the movie collection.
    """

    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        """List all movies in a structured, readable format."""
        movies = self._storage.list_movies()
        if movies:
            print("\n============================================================")
            print("                    🎬 My Movie Collection 🎬               ")
            print("============================================================")
            for title, details in movies.items():
                print(f"📽️  Title: {title}")
                print(f"📆  Year: {details['year']}")
                print(f"⭐  Rating: {details['rating']}/10")
                print(f"🖼️  Poster: {details['poster']}")
                print(f"🔗  IMDb: {details['link']}")
                print("------------------------------------------------------------")
        else:
            print("📭 Your movie collection is empty!")

    def _command_add_movie(self):
        """Add a new movie to the database by fetching from OMDb API with error handling."""
        title = input("Enter movie title: ")
        year = input("Enter movie year (optional, press Enter to skip): ")

        if not API_KEY:
            print("❌ ERROR: OMDB_API_KEY is missing! Check your .env file.")
            return

        title_encoded = quote_plus(title)
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title_encoded}"
        if year:
            url += f"&y={year}"

        try:
            response = requests.get(url, timeout=10)  # Add timeout to prevent hanging indefinitely
            response.raise_for_status()
            movie_data = response.json()

            if movie_data.get("Response") == "True":
                added = self._storage.add_movie(
                    title=movie_data["Title"],
                    year=movie_data["Year"],
                    rating=float(movie_data.get("imdbRating", 0)),
                    poster=movie_data.get("Poster", "N/A")
                )
                if added:
                    print(f"✅ '{movie_data['Title']}' added successfully!")
                else:
                    print(f"⚠️ '{movie_data['Title']}' is already in the collection.")
            else:
                print("❌ Movie not found. Please try another title or year.")
        except requests.exceptions.ConnectionError:
            print("❌ Error: Unable to connect to OMDb API. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: API request failed. {e}")

    def _command_delete_movie(self):
        """Delete a movie from the database."""
        title = input("Enter movie title to delete: ")
        result = self._storage.delete_movie(title)
        if result:
            print(f"🗑️ '{title}' removed successfully!")
        else:
            print(f"❌ Error: Movie '{title}' not found!")

    def _command_update_movie(self):
        """Update movie rating in the database."""
        title = input("Enter movie title to update: ")
        rating = input("Enter new rating (1-10): ")

        if not rating.strip():  # Check if the rating is empty
            print("❌ Error: Rating cannot be empty!")
            return

        try:
            rating = float(rating)
            if 1 <= rating <= 10:
                updated = self._storage.update_movie(title, rating)
                if updated:
                    print(f"✏️ '{title}' rating updated successfully!")
                else:
                    print(f"❌ Error: Movie '{title}' not found!")
            else:
                print("❌ Error: Rating must be between 1 and 10.")
        except ValueError:
            print("❌ Error: Invalid rating format! Please enter a number between 1 and 10.")

    def _command_movie_stats(self):
        """Show basic movie statistics, including the median rating."""
        movies = self._storage.list_movies()

        if movies:
            ratings = [details["rating"] for details in movies.values()]
            avg_rating = sum(ratings) / len(ratings)
            median_rating = statistics.median(ratings)  # ✅ Calculate median rating
            highest_rated = max(movies, key=lambda x: movies[x]["rating"])
            lowest_rated = min(movies, key=lambda x: movies[x]["rating"])

            print("\n📊 Movie Statistics:")
            print(f"⭐ Average Rating: {avg_rating:.2f}/10")
            print(f"📊 Median Rating: {median_rating:.2f}/10")  # ✅ Show median rating
            print(f"🏆 Highest Rated: {highest_rated} ({movies[highest_rated]['rating']}/10)")
            print(f"🐢 Lowest Rated: {lowest_rated} ({movies[lowest_rated]['rating']}/10)")
        else:
            print("📭 No movies available for statistics!")

    def _command_search_movie(self):
        """Search for a movie in the database."""
        query = input("Enter movie title to search: ").lower()
        movies = self._storage.list_movies()
        results = {k: v for k, v in movies.items() if query in k.lower()}
        if results:
            for title in results:
                print(f"🔍 {title} ({results[title]['year']}) - ⭐ {results[title]['rating']}/10")
        else:
            print("No matching movies found.")

    def _command_sorted_movies(self):
        """Sort movies by rating."""
        movies = self._storage.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        print("📋 Movies sorted by rating:")
        for title, details in sorted_movies:
            print(f"{title} - ⭐ {details['rating']}/10")

    def _generate_website(self):
        """
        Generate an HTML page displaying the movie collection with error handling.

        Uses an HTML template file instead of hardcoding HTML.
        """
        try:
            movies = self._storage.list_movies()
            if not movies:
                print("❌ No movies found. Add movies first before generating the website.")
                return

            # Read the HTML template file
            try:
                with open("static/index_template.html", "r", encoding="utf-8") as template_file:
                    template = template_file.read()
            except FileNotFoundError:
                print("❌ Error: HTML template file not found.")
                return

            # Generate movie cards HTML
            movie_cards_html = ""
            for title, details in movies.items():
                movie_cards_html += f"""
                <div class="movie-card">
                    <h2>{title}</h2>
                    <p>📆 {details['year']}</p>
                    <p>⭐ {details['rating']}/10</p>
                    <img src="{details['poster']}" alt="{title} Poster">
                    <p><a href="{details['link']}" target="_blank">🔗 IMDb Link</a></p>
                </div>
                """

            # Replace the placeholder with the movie cards HTML
            generated_html = template.replace("<!-- MOVIE_CARDS_PLACEHOLDER -->", movie_cards_html)

            # Write the generated HTML to the output file
            with open("data/movies.html", "w", encoding="utf-8") as file:
                file.write(generated_html)

            print("✅ Website generated successfully! Open 'movies.html' to view it.")
        except Exception as e:
            print(f"❌ Error: Failed to generate website. {e}")

    def _command_random_movie(self):
        """Pick and display a random movie from the collection."""
        movies = self._storage.list_movies()
        if not movies:
            print("📭 No movies available to pick from!")
            return
        random_movie = random.choice(list(movies.keys()))
        details = movies[random_movie]
        print("\n🎲 Random Movie Recommendation:")
        print(f"📽️  Title: {random_movie}")
        print(f"📆  Year: {details['year']}")
        print(f"⭐  Rating: {details['rating']}/10")
        print(f"🖼️  Poster: {details['poster']}")
        print(f"🔗  IMDb: {details['link']}")
        print("------------------------------------------------------------")

    def run(self):
        """Main application loop."""
        commands = {
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_sorted_movies,
            "9": self._generate_website

        }
        while True:
            print("\n********** My Movies Database **********")
            print(
                "0. Exit\n"
                "1. List movies\n"
                "2. Add movie\n"
                "3. Delete movie\n"
                "4. Update movie\n"
                "5. Stats\n"
                "6. Pick a random movie\n"
                "7. Search movie\n"
                "8. Movies sorted by rating\n"
                "9. Generate website\n")

            choice = input("Enter choice (0-9): ")
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice in commands:
                commands[choice]()
            else:
                print("❌ Invalid choice. Please try again.")

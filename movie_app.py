class MovieApp:
    """
    The MovieApp class handles user interaction and commands to manage the movie collection.
    """
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        """List all movies in the database."""
        movies = self._storage.list_movies()
        if movies:
            print("\n🎬 Your Movie Collection 🎬")
            print("=" * 50)
            for movie in movies:
                print(f"📽️ Title: {movie['title']}")
                print(f"📆 Year: {movie['year']}")
                print(f"⭐ Rating: {movie['rating']}/10")
                print(f"🖼️ Poster: {movie['poster']}")
                print(f"🔗 More Info: {movie['link']}")
                print("-" * 50)
        else:
            print("No movies found.")

    def _command_add_movie(self):
        """Add a new movie to the database."""
        title = input("Enter movie title: ")
        year = input("Enter release year: ")
        rating = input("Enter rating (1-10): ")
        self._storage.add_movie(title, int(year), float(rating))
        print(f"✅ '{title}' added successfully!")

    def _command_delete_movie(self):
        """Delete a movie from the database."""
        title = input("Enter movie title to delete: ")
        self._storage.delete_movie(title)
        print(f"🗑️ '{title}' removed successfully!")

    def _command_update_movie(self):
        """Update movie rating in the database."""
        title = input("Enter movie title to update: ")
        rating = input("Enter new rating (1-10): ")
        self._storage.update_movie(title, float(rating))
        print(f"✏️ '{title}' rating updated successfully!")

    def _generate_website(self):
        """Generate a static HTML page displaying the movie collection (Future Feature)."""
        print("🌐 Website generation is not implemented yet.")

    def run(self):
        """Main application loop to interact with the user."""
        while True:
            print("\n📽️ Movie App Menu 📽️")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie Rating")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

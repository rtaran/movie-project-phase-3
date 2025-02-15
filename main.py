from movie_app import MovieApp
from storage_json import StorageJson  # Change to StorageCsv if needed

# ✅ Initialize storage
storage = StorageJson("movies.json")  # Or use StorageCsv("movies.csv")

# ✅ Create the MovieApp instance
movie_app = MovieApp(storage)

# ✅ Run the application
if __name__ == "__main__":
    print("🚀 Starting Movie App...")
    movie_app.run()

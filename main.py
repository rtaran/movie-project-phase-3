import argparse
import os
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    """Main function that initializes the MovieApp with the appropriate storage file."""

    # ✅ Step 1: Use argparse to get the storage file from the command line
    parser = argparse.ArgumentParser(description="Movie Database App")
    parser.add_argument("storage_file", nargs="?", default="movies.json", help="Path to the storage file (JSON or CSV)")
    args = parser.parse_args()

    # ✅ Step 2: Determine storage type from file extension
    storage_file = args.storage_file
    file_extension = os.path.splitext(storage_file)[-1].lower()  # Get file extension

    if file_extension == ".json":
        storage = StorageJson(storage_file)  # Use JSON storage
    elif file_extension == ".csv":
        storage = StorageCsv(storage_file)  # Use CSV storage
    else:
        print("❌ ERROR: Unsupported file type. Use a JSON or CSV file.")
        return

    # ✅ Step 3: Start the MovieApp
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
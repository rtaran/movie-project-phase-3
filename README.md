# Movie Project - OOP + Web

## Overview
This project is a movie database application that allows users to manage their favorite movies using Object-Oriented Programming (OOP) principles. The application provides functionalities to store movie data in different formats (JSON, CSV) and generate a static web interface.

## Features
- **CRUD Operations**: Add, list, update, and delete movies
- **Multiple Storage Options**: Support for JSON and CSV storage
- **API Fetching**: Retrieve movie details automatically using the OMDb API
- **Web Interface**: Generate a static HTML webpage to display stored movies
- **GitHub Repository**: [Movie Project - Phase 3](https://github.com/rtaran/movie-project-phase-3.git)

## Architecture
The project follows an OOP-based design with the following key components:

- **IStorage (Interface)**: Defines the standard methods for storage operations
- **StorageJson (Class)**: Implements movie storage using JSON files
- **StorageCsv (Class)**: Implements movie storage using CSV files
- **Movie Manager**: Handles movie-related operations and interacts with the storage classes
- **Web Generator**: Generates a static HTML page from stored movie data (future feature)

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/rtaran/movie-project-phase-3.git
   cd movie-project-phase-3
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OMDb API key:
   ```plaintext
   OMDB_API_KEY=your_api_key_here
   ```
4. Run the program:
   ```bash
   python main.py
   ```

## Usage
- Add a movie (automatically fetches data from OMDb API):
  ```python
  storage.add_movie("Titanic")
  ```
- List movies:
  ```python
  print(storage.list_movies())
  ```
- Update a movie rating (not recommended since ratings are fetched automatically):
  ```python
  storage.update_movie("Titanic", 10)
  ```
- Delete a movie:
  ```python
  storage.delete_movie("Titanic")
  ```

## Future Enhancements
- Implement dynamic web UI with Flask/Django
- Improve API response handling and caching

## License
This project is licensed under the MIT License.

## Contributors
- RT
- Masterschool

---
Now the README reflects the **OMDb API integration**, making it more accurate! 🚀
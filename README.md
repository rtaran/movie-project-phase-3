# Movie Project - OOP + Web

## Overview
This project is a movie database application that allows users to manage their favorite movies using Object-Oriented Programming (OOP) principles. The application provides functionalities to store movie data in different formats (JSON, CSV) and generate a static web interface.

## Features
- **CRUD Operations**: Add, list, update, and delete movies
- **Multiple Storage Options**: Support for JSON storage (CSV implementation planned)
- **API Fetching**: Retrieve movie details automatically using an external API (future feature)
- **Web Interface**: Generate a static HTML webpage to display stored movies
- **GitHub Repository**: [Movie Project - Phase 3](https://github.com/rtaran/movie-project-phase-3.git)

## Architecture
The project follows an OOP-based design with the following key components:

- **IStorage (Interface)**: Defines the standard methods for storage operations
- **StorageJson (Class)**: Implements movie storage using JSON files
- **StorageCsv (Class - Planned)**: Future support for storing movies in CSV format
- **Movie Manager**: Handles movie-related operations and interacts with the storage classes
- **Web Generator**: Generates a static HTML page from stored movie data (future feature)

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/rtaran/movie-project-phase-3.git
   cd movie-project-phase-3
   ```
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python main.py
   ```

## Usage
- Add a movie:
  ```python
  storage.add_movie("Titanic", 1997, 9, "https://example.com/titanic.jpg")
  ```
- List movies:
  ```python
  print(storage.list_movies())
  ```
- Update a movie rating:
  ```python
  storage.update_movie("Titanic", 10)
  ```
- Delete a movie:
  ```python
  storage.delete_movie("Titanic")
  ```

## Future Enhancements
- Implement CSV storage
- Fetch movie data from an API automatically
- Create a dynamic web UI with Flask/Django

## License
This project is licensed under the MIT License.

## Contributors
- RT
- Masterschool


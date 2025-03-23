# Library Management API

A simple RESTful API for managing books in a library. The application allows you to:

- Add a new book
- Delete a book
- Fetch a list of all books
- Borrow a book
- Return a book

The project uses FastAPI as the web framework and PostgreSQL as the database, all containerized with Docker and Docker Compose.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing via HTML Page](#testing-via-html-page)
- [Database Visualization](#database-visualization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- CRUD for books (create, read, update - borrow/return, and delete)
- PostgreSQL integration
- Docker Compose setup for easy local development
- FastAPI framework providing automatic docs and interactive Swagger UI

## Tech Stack

- Python (3.10)
- FastAPI (for REST endpoints)
- Uvicorn (ASGI server)
- PostgreSQL (database)
- Docker & Docker Compose

## Project Structure

A possible structure (if you followed a modular approach) might look like this:

.  
 ├── app/  
 │ ├── init.py  
 │ ├── main.py # FastAPI app creation and router registration  
 │ ├── db.py # Database engine & session configuration  
 │ ├── models.py # SQLAlchemy models  
 │ ├── schemas.py # Pydantic schemas  
 │ ├── dependencies.py # Shared dependencies (e.g. get_db)  
 │ └── routers/  
 │ ├── init.py  
 │ └── books.py # Book endpoints (create, read, borrow, return, delete)  
 ├── docker-compose.yml  
 ├── Dockerfile  
 ├── requirements.txt  
 └── README.md

If you have a single-file approach, you may only have something like main.py, docker-compose.yml, Dockerfile, and requirements.txt. Either way, the usage is similar.

## Installation

Clone the repository or download the project files into a local folder.
Make sure you have Docker and Docker Compose installed on your system.
(Optional) Update environment variables in docker-compose.yml if you want to change the database name, user, or password.

## Usage

Build and run containers:
docker compose up --build

This will:

Launch a PostgreSQL container (listening on port 5432).
Build a Python (FastAPI) image from the Dockerfile and run it (listening on port 8000).
Check the logs to see if both containers (library_db and library_api) have started properly.
Access the API (Swagger UI) in your browser at:
http://localhost:8000/docs
Shut down the containers with CTRL + C or:
docker compose down

## API Endpoints

Below is a summary of the main routes:

Endpoint: /books
Method: POST
Description: Add a new book
Body / Params:
{ "serial_number": "xxxxxx", "title": "...", "author": "..." } Response: Returns the created book (JSON)

Endpoint: /books
Method: GET
Description: Get all books
Body / Params: None
Response: Returns a list of all books

Endpoint: /books/{serial_number}
Method: DELETE
Description: Delete a book by serial number
Body / Params: None
Response: { "message": "Book deleted..." }

Endpoint: /books/{serial_number}/borrow
Method: PUT
Description: Borrow a book
Body / Params:
{ "library_card_number": "xxxxxx" } Response: Returns the updated book (JSON)

Endpoint: /books/{serial_number}/return
Method: PUT
Description: Return a borrowed book
Body / Params: None
Response: Returns the updated book (JSON)

Notes:

Serial numbers and library card numbers are 6-digit numeric strings ("123456", etc.).
The API expects and returns JSON.

## Testing

I have included a simple HTML file for testing (e.g. index.html), you can open it in your browser (e.g. file://...) and interact with the forms that send requests to the API endpoints:

Make sure the line: const baseUrl = 'http://localhost:8000'; is correct for your setup.
Fill out the forms (Add Book, Delete Book, Borrow Book, Return Book) and click the corresponding buttons.
View the API response in the output panel on the page.

It is possible to test the API using http://localhost:8000/docs as well.

## Database Visualization

To inspect the PostgreSQL database outside of the API, you can connect using tools such as DBVisualizer or pgAdmin.
Make sure your DB connection settings match those in docker-compose.yml:

Host: localhost
Port: 5432
Database: library_db
User: library_user
Password: library_password
If you see an error like relation "books" does not exist, ensure you are connected to the correct database and schema (public).

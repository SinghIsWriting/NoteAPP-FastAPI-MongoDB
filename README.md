# Note App

A simple and efficient Note Management Application built using **FastAPI** and **MongoDB**. This application allows users to create, read, update, and delete notes with additional features like marking notes as important.

## Deployed App Link: https://fastnote.devhome.me

## Features

- **Create Notes**: Add new notes with a title, content, and an optional "important" flag.
- **View Notes**: View all notes in a user-friendly interface.
- **Update Notes**: Edit existing notes, including their title, content, and importance.
- **Delete Notes**: Remove notes from the database.
- **View Note Details**: Fetch detailed information about a specific note.

## Technologies Used

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance) web framework for Python.
- **Database**: [MongoDB](https://www.mongodb.com/) - A NoSQL database for storing notes.
- **Frontend**: Jinja2 templates for rendering HTML pages.
- **Other Libraries**:
  - `pymongo` for MongoDB integration.
  - `bson` for handling MongoDB ObjectIds.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.12 or higher
- MongoDB (running locally or on a cloud service like MongoDB Atlas)
- `pip` (Python package manager)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SinghIsWriting/NoteAPP-FastAPI-MongoDB.git
   cd NoteAPP-FastAPI-MongoDB
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up MongoDB**:
   - Ensure MongoDB is running locally or provide a connection string for a remote MongoDB instance.
   - Update the `config/db.py` file with your MongoDB connection details.

5. **Run the Application**:
   ```bash
   uvicorn routes.note:note_router --reload
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Project Structure

```
Fast API/
├── config/
│   └── db.py              # MongoDB connection configuration
├── models/
│   └── note.py            # Note model definition
├── routes/
│   └── note.py            # API routes for note operations
├── schemas/
│   └── note.py            # Schema for note serialization
├── templates/
│   ├── index.html         # Form for adding notes
│   ├── notes.html         # Page for displaying notes
├── static/                # Static files (CSS, JS, etc.)
├── README.md              # Project documentation
├── index.py             
├── .gitignore             
├── LICENSE             
└── requirements.txt       # Required packages file
```

## API Endpoints

### 1. **GET** `/`
- **Description**: Render the form for adding a new note.
- **Response**: HTML page.

### 2. **GET** `/notes`
- **Description**: Fetch and display all notes.
- **Response**: HTML page with a list of notes.

### 3. **POST** `/`
- **Description**: Add a new note.
- **Request Body**: Form data (`title`, `note`, `important`).
- **Response**: HTML page with updated notes.

### 4. **PUT** `/update`
- **Description**: Update an existing note.
- **Request Body**: JSON (`id`, `title`, `note`, `important`).
- **Response**: JSON with status and message.

### 5. **DELETE** `/delete`
- **Description**: Delete a note.
- **Request Body**: JSON (`id`).
- **Response**: JSON with status and message.

### 6. **GET** `/details/{id}`
- **Description**: Fetch details of a specific note.
- **Response**: JSON with note details.

## Screenshots

### Home Page
![Home Page - NoteApp-FastAPI-1](https://github.com/user-attachments/assets/6dc7a3e7-8623-4459-be06-57689769aef5)


### Notes List
![Notes List - NoteApp-FastAPI-2](https://github.com/user-attachments/assets/80487786-202c-4eda-89ca-bdf45ec87528)


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Contact Me**

For any inquiries or support, please reach out to:
- **Name**: Abhishek Singh
- **Email**: sabhisheksingh343204@gmail.com
- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/abhishek-singh-bba2662a9)
- **Portfolio**: [Abhishek Singh](https://portfolio-abhishek-singh-nine.vercel.app/)

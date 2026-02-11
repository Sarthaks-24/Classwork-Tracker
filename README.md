# Classwork Tracker

Classwork Tracker is a Flask-based web application built to explore backend workflows for file distribution and structured metadata management. The system allows teachers to upload assignment PDFs while students retrieve them through filtered search. Firebase Firestore is used for metadata storage, and the Dropbox API handles cloud-based file persistence.

---

## Features

### Teacher Portal
- Registration and login system for secure access  
- Upload assignment PDFs with metadata (Class, Section, Subject, Date, Notes)  
- Automatic file naming based on metadata for consistent organization  

### Student Portal
- Filter assignments using Class, Section, Subject, and Date  
- View or download files directly through generated links  

### Cloud Integration
- Firebase Firestore for storing assignment metadata and user data  
- Dropbox API for managing file uploads and storage  

---

## Tech Stack

- **Backend**: Python (Flask)  
- **Database**: Firebase Firestore  
- **File Storage**: Dropbox API  
- **Frontend**: HTML, CSS (Jinja2 templating)  

### Dependencies
- `firebase-admin`  
- `dropbox`  
- `python-dotenv`  

---

## Design Notes

- Firestore was chosen for flexible document-based storage of assignment metadata.  
- Dropbox API simulates real-world cloud storage instead of relying on local files.  
- Automatic file naming reduces manual errors during uploads.  
- The project focuses on API integration, authentication flow, and debugging third-party services.

---

## Prerequisites

- Python 3.x installed  
- Firebase project with Service Account JSON  
- Dropbox developer app with Refresh Token, App Key, and App Secret  

---

## Installation

### 1. Clone the repository
```bash
git clone <repository_url>
cd Classwork-Tracker
```

### 2. Create a virtual environment (optional)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a .env file in the root directory:

```env
FIREBASE_SDK=path/to/firebase-adminsdk.json
REFRESH_TOKEN=your_dropbox_refresh_token
API_KEY=your_dropbox_app_key
API_SECRET=your_dropbox_app_secret
```

## Usage
Run the application:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

## Project Structure
- **app.py** — Main Flask application defining routes and views
- **functions.py** — Firebase and Dropbox helper logic
- **templates/** — Jinja2 HTML templates
- **static/** — CSS and static assets
- **requirements.txt** — Project dependencies

## Future Improvements
- Role-based authentication and permissions
- Improved error handling for failed uploads
- Pagination for large assignment lists

## Author
Made by Sarthak Suri

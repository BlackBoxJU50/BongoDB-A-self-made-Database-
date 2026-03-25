# BongoAuth Sample Website

This is a demonstration of how to build a full user authentication system (Signup, Login, Profile) using **BongoDB** as the backend database.

## Features
- **Signup**: Users can register with their name, email, password, and a profile image.
- **Image Handling**: User data is stored in BongoDB, while profile images are stored locally in `static/uploads/`.
- **Login**: Verification of credentials against the BongoDB "Users" collection.
- **Profile**: A premium profile page showing the user's information and their uploaded image.

## Setup Instructions

### 1. Requirements
Ensure you have the following installed:
```bash
pip install flask requests
```

### 2. Start BongoDB
BongoDB must be running in the background to handle the database requests.
```bash
# In the BongoDB root directory
python3 main.py
```
*Note: Make sure BongoDB is authenticated and running on port 5001.*

### 3. Start the Sample Website
In a new terminal:
```bash
cd test_website
python3 app.py
```
*The website will be available at http://localhost:5002.*

## How it Works with BongoDB

### Signup
When a user signs up, the website:
1. Saves the image to `test_website/static/uploads/`.
2. Sends a `POST` request to BongoDB's `/api/v1/insert` endpoint with the user details and the local image URL.
3. BongoDB automatically creates a "Users" sheet in your Google Spreadsheet (if it doesn't exist) and inserts the row.

### Login
The website:
1. Sends a `GET` request to BongoDB's `/api/v1/find?collection=Users`.
2. Browses the returned JSON list to find a matching email and password.
3. If found, starts a session and redirects to the profile.

## Project Structure
- `app.py`: Main Flask application logic.
- `static/uploads/`: Folder where profile images are stored.
- `templates/`: Premium glassmorphism HTML templates.

# 📸 Instagram Clone -- Django Project

A fully functional Instagram-like web application built using
**Django**, featuring user authentication, profiles, posts, likes,
comments, and more.

## 🚀 Features

### 👤 User & Profile

-   User registration & login
-   Profile picture upload
-   Edit profile (bio, image, username)
-   Follow / Unfollow system

### 🖼️ Posts

-   Create new posts with images
-   View posts on homepage feed
-   Like / Unlike posts
-   Comment on posts
-   Post detail page with comments section

## 🏗️ Tech Stack

### Backend

-   Django
-   Django ORM
-   Django Authentication

### Frontend

-   HTML, CSS, JavaScript
-   Bootstrap / TailwindCSS

### Database

-   SQLite (default)

## 📁 Project Structure

    instaclone/
    ├── core/
    ├── accounts/
    ├── posts/
    ├── static/
    ├── templates/
    ├── media/
    └── manage.py

## 🔧 Installation & Setup

### 1. Clone the repository

    git clone https://github.com/yourusername/instagram-clone.git
    cd instagram-clone

### 2. Create virtual environment

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate    # Windows

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Run migrations

    python manage.py migrate

### 5. Create superuser

    python manage.py createsuperuser

### 6. Start server

    python manage.py runserver

Visit: http://127.0.0.1:8000/

## 🛠️ Future Improvements

-   Messaging system
-   Stories feature
-   Explore recommendations
-   Real-time notifications
-   REST API with DRF

## 📝 License

MIT License

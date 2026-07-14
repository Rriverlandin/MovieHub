# MovieHub

#### Video Link: https://youtu.be/yqp1-_fi2gw

#### GitHub: Rriverlandin

## Description

MovieHub is a web application that allows users to build and manage their own personal movie collection. Instead of keeping track of movies in notes or trying to remember which movies they have already watched, MovieHub provides a clean and organized library where users can store all their favorite films.

Users can create an account, securely log in, and manage their own private movie collection. Each user has access to a personal dashboard where they can add new movies, edit existing entries, delete movies, rate them from 1 to 10, mark them as watched, and save them to their favorites.

One of the main goals of this project was to create an application that feels modern rather than a simple CRUD project. For that reason, I focused heavily on the user experience by implementing animations, modal windows, responsive layouts, and a dark theme inspired by modern streaming platforms.

MovieHub was developed as the final project for Harvard's CS50x course using Flask and SQLite. Building this application allowed me to combine many of the concepts taught throughout the course, including Python programming, databases, authentication, and web development.

---

## Features

* User registration and authentication
* Secure password hashing
* Private movie libraries for each user
* Add, edit, and delete movies
* Mark movies as watched
* Add movies to favorites
* Rate movies from 1 to 10
* Instant search by title or genre
* Responsive dark-themed design
* Animated modal windows and interactive UI

---

## Technologies Used

* Python
* Flask
* SQLite
* SQLAlchemy
* HTML5
* CSS3
* JavaScript
* Jinja2

---

## Project Structure

```text
project/
│
├── instance/
│   └── moviehub.db
│
├── static/
│   ├── dashboard.js
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── dashboard.html
│   ├── error.html
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   └── register.html
│
├── app.py
├── models.py
├── requirements.txt
└── seed.py
```

---

## Design Decisions

While designing MovieHub, I wanted the project to be easy to maintain and follow Flask's recommended structure.

The application logic is handled in `app.py`, where routing, authentication, and CRUD operations are implemented. Database models are separated into `models.py`, making the code cleaner and easier to extend.

HTML templates are stored inside the `templates` directory and use Jinja2 template inheritance. Shared components such as the navigation bar, footer, and page layout are defined in `layout.html`, while individual pages extend this base template.

The frontend is separated into CSS and JavaScript files inside the `static` directory. All styling was written using custom CSS without relying on external UI frameworks. JavaScript is used where necessary, such as for instant searching and animated modal windows.

Another important design decision was creating a `seed.py` script. This script automatically creates a demo account and fills the database with sample movies, making it easier to demonstrate the application's features.

SQLite and SQLAlchemy were chosen because they integrate naturally with Flask, require no external database server, and are well suited for a personal movie collection application.

---

## Running the Project

To run the project locally:

```bash
python seed.py
python app.py
```

Demo account:

```text
Username: demo
Password: demo1234
```

---

## Future Improvements

Features planned for future versions include:

* Automatic movie posters fetched from an API
* Watchlist support
* Movie reviews
* Advanced sorting and filtering
* Statistics dashboard
* Dark and light theme switching
* Importing movies from IMDb or Letterboxd
* User profile customization

---

## Why I Built This Project

I chose to build MovieHub because movies are something many people enjoy, and I wanted to create an application that combines database management, authentication, and modern frontend design.

This project allowed me to apply everything I learned throughout CS50x, from Python and SQL to Flask, HTML, CSS, and JavaScript.

---

## Author

Created by Zehra Nehir Macar as the final project for Harvard's CS50x course.

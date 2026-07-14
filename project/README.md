# MovieHub

#### Video Demo: https://youtu.be/YOUR_VIDEO_LINK

#### GitHub: https://github.com/Rriverlandin

## Description

MovieHub is a web application that allows users to build and manage their own personal movie collection. Instead of keeping track of movies in notes or trying to remember what has already been watched, MovieHub provides a clean and organized place to store every movie in one place.

The application allows users to create an account, securely log in, and manage a private movie library. Each user has their own dashboard where they can add new movies, edit existing entries, delete movies, rate them from 1 to 10, mark them as watched, and add them to their favorites.

One of my main goals while building this project was to create an application that feels modern rather than a traditional CRUD application. Because of that, I focused heavily on the user interface by adding animations, modal windows, responsive layouts, and a dark theme inspired by modern streaming services.

MovieHub was developed as my final project for Harvard's CS50x course using Flask and SQLite. Building this project allowed me to combine many of the concepts covered throughout the course, including Python, SQL, authentication, and web development.

---

## Features

* User registration and authentication
* Secure password hashing
* Individual movie collections for every user
* Add new movies
* Edit movie information
* Delete movies
* Mark movies as watched
* Add movies to favorites
* Rate movies from 1 to 10
* Search movies instantly by title or genre
* Responsive dark-themed interface
* Animated modal forms and interactive UI

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

While designing MovieHub, I wanted the project to be maintainable and follow Flask's recommended structure.

The application logic is handled in `app.py`, where routing, authentication, and CRUD operations are implemented. Database models are separated into `models.py`, making the code cleaner and easier to extend in the future.

HTML templates are stored inside the `templates` directory and use Jinja2 template inheritance. Shared components such as the navigation bar, footer, and overall page layout are defined in `layout.html`, while each page extends this base template.

The frontend is separated into CSS and JavaScript files inside the `static` directory. All styling was written using custom CSS without relying on external UI frameworks. JavaScript is used only where necessary, such as for instant movie searching and controlling animated modal windows.

Another important design decision was creating a `seed.py` file. This script automatically creates a demo account with sample movies, making it easier to demonstrate the application's functionality without manually entering data.

For the database layer, I chose SQLite together with SQLAlchemy because they integrate naturally with Flask, require no external database server, and are well suited for a personal movie collection application.

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

Features I would like to add in future versions include:

* Automatic movie posters fetched from an API
* Watchlist support
* Movie reviews and comments
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

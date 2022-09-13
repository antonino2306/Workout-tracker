# Workout Tracker
## Video Demo:  <https://youtu.be/_8g7yMm6rXE>
### Description:
Workout Tracker is a web-based application made using **HTML**, **CSS** and **JavaScript** for the front-end and the Python framework **Flask** for the back-end.

#### Structure of the project folder:

  - `app.py` is the main file
  - `functions.py` contains functions used in `app.py`
  - `/templates` folder contains all the html files
  - `/static` folder contains stylesheet files, javascript files and a file with the queries used to create the database and search for data in it
  - In `requirements.txt` there is a list of all the module used in the project

#### `app.py`:
`app.py` is the main file of the project.

- First we imported the Flask class. Next we create an instance of this class. The first argument is the name of the application’s module or package. ` __name__ ` is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows where to look for resources such as templates and static files. 
- Lines 15 - 17: Configure the session of a user using filesystem instead of cookies.
- Line 20: configuration of the sqlite database
- From line 31 there are all the routes of the web applications. Most of them are preceded by `@login_required`. This decorator allows user to access to these pages only after registration or login and see his personal information.

#### `functions.py`
- Contains the function to create the decorator for the requirement of the login to access to the personal area of the web app.
  
#### `/templates`:


- `layout.html` is the base template for all the other pages. In the head of this file there is the link to:
  
    - Google fonts API
    - Fontawesome for the icons
    - Bootstrap
    - stylesheet file in the `/static` folder \(it's only one file for all pages).

    I use jinja2 syntax to:

    - Change the title of the page in every tab
    - Display the navigation bar only if the user is logged in
    - Create a block for the main content and a block for the scripts
    
    All the other files in this directory are based on the model of `layout.html`

#### `/static`:

- `style.css`: contains all the css rules to create the layout of the web app. I use media queries to set light or dark mode according to user's browser settings and to make the page responsive

- `add_exercise.js`: contains a script used in `scheda.html` and `add_ex.html` to dynamically add a new row to insert a new exercise in the workout.

- `query.sql` contains all the queries used to create the table of the database and the most complicated select query that gives in output all the workouts of an user.

#### `Workout.db`:

The database consists of four tables:

1. `CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL,
    height INTEGER,
    weight INTEGER,
    hash TEXT NOT NULL
);`
2. `CREATE TABLE IF NOT EXISTS exercises
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    muscles TEXT,
    tutorial TEXT
);`
3. `CREATE TABLE IF NOT EXISTS programs
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE (name, user_id)
    FOREIGN KEY (user_id) REFERENCES users(id)
);`
4. `CREATE TABLE IF NOT EXISTS workouts
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    program_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    rest INTEGER NOT NULL,
    weight INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);`

To obtain in output all the programs of an user I used a multiple JOIN among programs, workouts and exercises tables using as condition the user_id assigned to the programs.

#### Design:
- Font: Montserrat
- Color palette: The background color is `#fffaffff` for light mode and `#00111C` for dark mode. The text color is `#00111C` for light mode and `#fffaffff` for dark mode.
- The workouts in the main page and the forms to add exercises are rendered as a table made using a grid layout because it is easier to adapt to different screens' size than an HTML table.



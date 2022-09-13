CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL,
    height INTEGER,
    weight INTEGER,
    hash TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS exercises
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    muscles TEXT,
    tutorial TEXT
);

CREATE TABLE IF NOT EXISTS programs
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE (name, user_id)
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS workouts
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
);

-- select query to obtain workouts output in index
SELECT p.name AS "program", e.name, w.sets, w.reps, w.rest, w.weight 
FROM programs AS p
JOIN workouts AS w ON p.id = w.program_id
JOIN exercises AS e ON e.id = w.exercise_id
WHERE p.user_id = 1;

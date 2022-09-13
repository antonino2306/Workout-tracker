from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functions import login_required



app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///workout.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    scheda = db.execute("""SELECT p.name AS "program", e.name, w.sets, w.reps, w.rest, w.weight  
                        FROM programs AS p
                        JOIN workouts AS w ON p.id = w.program_id
                        JOIN exercises AS e ON e.id = w.exercise_id
                        WHERE p.user_id = ?""", session['user_id'])

    programs = db.execute("SELECT DISTINCT(name) FROM programs WHERE user_id = ?", session['user_id'])

    return render_template("index.html", programs=programs, scheda=scheda, p_lenght=len(programs))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Get all the users already registered
    user_list = db.execute("SELECT username FROM users")

    # POST
    if request.method == "POST":

        # Get all the data from the form
        username = request.form.get("username").strip()
        age = int(request.form.get("age").strip())
        height = int(request.form.get("height").strip())
        weight = int(request.form.get("weight").strip())
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validation of form's values
        if len(username) == 0:
            return render_template("error.html", error="Insert username" )
        
        if not type(age) == int:
            return render_template("error.html", error="Invalid age")

        if not type(height) == int:
            return render_template("error.html", error="Invalid height")

        if not type(weight) == int:
            return render_template("error.html", error="Invalid weight")
        
        if len(password) == 0 or len(confirmation) == 0:
            return render_template("error.html", error="Missing password")

        if any(user["username"] == username for user in user_list):
            return render_template("error.html", error="This username already exists")

        else:
            if password == confirmation:

                # Generate the hash of the password for more safety
                pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

                # Insert the user in the database
                db.execute("INSERT INTO users (username, age, height, weight, hash) VALUES (?, ?, ?, ?, ?)", username, age, height, weight, pw_hash)
                
                return redirect("/")

            else:
                return render_template("error.html", error="Passwords doesn't match")

    # GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", error="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").strip())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", error="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    # Select all the user's info
    info = db.execute("SELECT username, age, height, weight FROM users WHERE id = ?", session['user_id'])
    return render_template("profile.html", info=info)


@app.route("/scheda", methods=["GET", "POST"])
@login_required
def scheda():
    exercises = db.execute("SELECT name, muscles FROM exercises")
    e = []

    for r in exercises:
        e.append(r['name'].lower())

    if request.method == "POST":

        programs = db.execute("SELECT name FROM programs WHERE user_id = ?", session['user_id'])

        program_name = request.form.get("name")

        for program in programs:
            if program_name == program['name']:
                return render_template("error.html", error="This program already exists")


        workout = []
        counter = 0
        while request.form.get(f"exercise-name-{counter}") != None:
            row = {}
            row['name'] = request.form.get(f"exercise-name-{counter}").lower()
            row['sets'] = request.form.get(f"sets-{counter}")        
            row['reps'] = request.form.get(f"reps-{counter}")        
            row['rest'] = request.form.get(f"rest-{counter}")

            if len(row['name']) != 0 and len(row['sets']) != 0 and len(row['reps']) != 0 and len(row['rest']) != 0:
                workout.append(row)
            
            counter += 1

        if len(workout) != 0:
            db.execute("INSERT INTO programs (name, user_id) VALUES (?, ?)", program_name, session['user_id'])
            
            program_id = db.execute("SELECT id FROM programs WHERE name = ? AND user_id = ?", program_name, session['user_id'])
            
            for exercise in workout:
                if exercise['name'] in e:
                    
                    exercise_id = db.execute("SELECT id FROM exercises WHERE name = ?", exercise['name'])
                    
                    db.execute("INSERT INTO workouts (program_id, exercise_id, sets, reps, rest) VALUES (?, ?, ?, ?, ?)", program_id[0]["id"], exercise_id[0]["id"], exercise["sets"], exercise["reps"], exercise["rest"])
                else:
                    return render_template("error.html", error="This exercise doesn't exists")
            
            return redirect("/")

    # method == GET
    else:
        return render_template("scheda.html", exercises=exercises)


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():

    # Get form's data
    new_password = request.form.get("new_password")
    confirmation = request.form.get("confirmation")

    # Check form's data
    if len(new_password) == 0 or len(confirmation) == 0:
        return render_template("error.html", error="Insert password")

    if not new_password == confirmation:
        return render_template("error.html", error="Passwords don't match")

    # Generate new hash 
    pw_hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)

    db.execute("UPDATE users SET hash = ? WHERE id = ?", pw_hash, session['user_id'])

    return redirect("/login")



@app.route("/info_update", methods=["GET", "POST"])
@login_required
def info_update():
    
    if request.method == 'POST':

        # Get user's data
        age = int(request.form.get("age"))
        height = int(request.form.get("height"))
        weight = int(request.form.get("weight"))

        # Check data
        if not type(age) == int:
            return render_template("error.html", error="Invalid age")

        if not type(height) == int:
            return render_template("error.html", error="Invalid height")

        if not type(weight) == int:
            return render_template("error.html", error="Invalid weight")

        db.execute("UPDATE users SET age = ?, height = ?, weight = ?", age, height, weight)
        
        return redirect("/profile")

    else:
        return render_template("info_update.html")


@app.route("/program_delete", methods=["GET", "POST"])
@login_required
def program_delete():
    
    program_name = request.form.get("program")
    
    # Returns a list of dict
    program_id = db.execute("SELECT id FROM programs WHERE name = ? AND user_id = ?", program_name, session['user_id'])

    # Delete first the data from workouts and then from programs to preserve referencial integrity
    db.execute("DELETE FROM workouts WHERE program_id = ?", program_id[0]['id'])
    db.execute("DELETE FROM programs WHERE name = ? AND user_id = ?", program_name, session['user_id'])

    return redirect("/")

@app.route("/program_update", methods=["GET", "POST"])
@login_required
def program_update():

    program_name = request.args.get("program")

    # Select program info from the database and then pass them to the web page
    scheda = db.execute("""SELECT e.name, w.sets, w.reps, w.rest, w.weight  
                    FROM programs AS p
                    JOIN workouts AS w ON p.id = w.program_id
                    JOIN exercises AS e ON e.id = w.exercise_id
                    WHERE p.user_id = ? AND p.name = ?""", session['user_id'], program_name)

    return render_template("program_update.html", program_name=program_name, scheda=scheda)


@app.route('/delete_ex', methods=['POST', 'GET'])
@login_required
def delete_ex():

    # Get data from the form
    program_name = request.form.get("program")
    counter = int(request.form.get('counter'))
    exercise = request.form.get(f"exercise-{counter}")
    
    program_id = db.execute("SELECT id FROM programs WHERE name = ? AND user_id = ?", program_name, session['user_id'])
    exercise_id = db.execute("SELECT id FROM exercises WHERE name = ?", exercise)
    
    # Delete the exercise
    db.execute("""DELETE FROM workouts
                WHERE program_id = ? AND exercise_id = ?""", program_id[0]['id'], exercise_id[0]['id'])

    return redirect(f"/program_update?program={program_name}")


@app.route("/add_ex", methods=["GET", "POST"])
@login_required
def add_ex():
    
    program_name = request.args.get("program")
    
    exercise_list = db.execute("SELECT name, muscles FROM exercises")
    e = []

    for r in exercise_list:
        e.append(r['name'].lower())
    
    if request.method == 'POST':
        

        program_name = request.form.get("program")
        adding_list = []
        counter = 0
        while request.form.get(f"exercise-name-{counter}") != None:
            row = {}
            row['name'] = request.form.get(f"exercise-name-{counter}").lower()
            row['sets'] = request.form.get(f"sets-{counter}")        
            row['reps'] = request.form.get(f"reps-{counter}")        
            row['rest'] = request.form.get(f"rest-{counter}")

            if len(row['name']) != 0 and len(row['sets']) != 0 and len(row['reps']) != 0 and len(row['rest']) != 0:
                adding_list.append(row)
            
            counter += 1

            if len(adding_list) != 0:
                program_id = db.execute("SELECT id FROM programs WHERE name = ? AND user_id = ?", program_name, session['user_id'])    
                exercises = db.execute("SELECT exercise_id FROM workouts WHERE program_id = ?", program_id[0]['id'])
                for row in adding_list:

                    if row['name'] in e:
                        exercise_id = db.execute("SELECT id FROM exercises WHERE name = ?", row['name'])
                    
                        if any(ex['exercise_id'] == exercise_id[0]['id'] for ex in exercises):

                            db.execute("UPDATE workouts SET sets = ?, reps = ?, rest = ? WHERE exercise_id = ? AND program_id = ?", row['sets'], row['reps'], row['rest'], exercise_id[0]['id'], program_id[0]['id'])

                        else:

                            db.execute("INSERT INTO workouts (program_id, exercise_id, sets, reps, rest) VALUES (?, ?, ?, ?, ?)", program_id[0]["id"], exercise_id[0]["id"], row["sets"], row["reps"], row["rest"])
                    
                    else:
                        return render_template("error.html", error="Could not find exercise")

        return redirect(f"/program_update?program={program_name}")

    # Method Get
    else:
        return render_template("add_ex.html", program_name=program_name, exercises=exercise_list)
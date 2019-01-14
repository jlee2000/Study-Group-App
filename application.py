import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database called studyspace.db
db = SQL("sqlite:///studyspace.db")


@app.route("/")
@login_required
def index():
    # Select all active study sessions
    studysesh = db.execute("SELECT * FROM studysessions WHERE isactive == 1")
    ratings = []

    # Append ratings from each active study session to the array 'ratings' and sort array
    for seshs in studysesh:
        ratings.append(seshs['rating'])
    ratings.sort()

    # Remove ratings until only the highest 3 are left
    while len(ratings) > 3:
        ratings.pop(0)
    topsesh = []

    # Iterate through ratings
    for rating in ratings:
        for item in studysesh:

            # If a session has the same rating as a top rating, append to the array 'topsesh'
            if item["rating"] == rating:
                topsesh.append(item)
        studysesh[:] = [d for d in studysesh if not (d.get('rating') == rating)]

    # Limit number of the top three sessions to 3
    while len(topsesh) > 3:
        topsesh.pop()
    return render_template("index.html", topsesh=topsesh)


@app.route("/map")
@login_required
def gmap():
    # Select locations of all active study study sessions, and pass that array to the live map
    studysesh = db.execute("SELECT location FROM studysessions WHERE isactive == 1")
    return render_template("map.html", studysesh=studysesh)


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Use database insertion method from register
    username = request.args.get("username")

    # Checks validity of username
    if len(username) == 0:
        return jsonify(False)

    # Checks if username exists in the database
    stmt = db.execute("SELECT username FROM users WHERE username = :username",
                      username=username)
    if not stmt:
        return jsonify(True)
    return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Stores username, password, and password confirmation
        username = request.form.get("username")

        # Checks validity of username
        if len(username) == 0:
            return apology("Username too short")
        stmt = db.execute("SELECT username FROM users WHERE username = :username",
                          username=username)
        if stmt:
            return apology("User already exists")

        # Checks validity of password
        pw = request.form.get("password")
        confirmpw = request.form.get("confirmation")
        if not username:
            return apology("Missing username")
        elif not pw:
            return apology("Missing password")
        elif not confirmpw:
            return apology("Please confirm password")
        elif pw != confirmpw:
            return apology("Passwords do not match")
        # Hashes password
        hash = generate_password_hash(pw)
        # Inserts user and password into database
        stmt = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                          username=username, hash=hash)
        if not stmt:
            return apology("User already exists in the database")
        # Stores user id to the active session (logs them in automatically)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


@app.route("/makesession", methods=["GET", "POST"])
@login_required
def makesession():

    # Checks if data was posted, else loads form
    if request.method == "POST":

        # Retrieves user input from form
        name = request.form.get("name")
        description = request.form.get("description")
        building = request.form.get("building")
        city = request.form.get("city")
        state = request.form.get("state")

        # Creates a string out of location input from user
        location = building.strip() + ", " + city.strip() + ", " + state.strip()

        # Insert study session into database
        stmt = db.execute("INSERT INTO studysessions (name, description, building, location, isactive, rating, userid) VALUES (:name, :description, :building, :location, :isactive, :rating, :userid)",
                          name=name, description=description, building=building, location=location, isactive=1, rating=5, userid=session["user_id"])
        return redirect("/")
    else:
        return render_template("makesession.html")


@app.route("/leavereview", methods=["GET", "POST"])
@login_required
def leavereview():
    # Checks if data was posted, else redirects to index
    if request.method == "POST":

        # Retrieves user input from form
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        # Retrieves studysessionid from URL
        studysessionid = request.form.get("sp_id")

        # Insert study session into database
        stmt = db.execute("INSERT INTO ratings (userid, studysessionid, rating, comment, timestamp) VALUES (:userid, :studysessionid, :rating, :comment, datetime(strftime('%s','now'), 'unixepoch'))",
                          userid=session["user_id"], studysessionid=studysessionid, rating=rating, comment=comment)

        # Selecst average rating from all reviews with studysessionid matching the id of the respective studysession
        statement = db.execute("SELECT avg(rating) FROM ratings WHERE studysessionid = :id",
                               id=studysessionid)

        # Updates rating for current study session in the studysessions database
        stmt1 = db.execute("UPDATE studysessions SET rating = :star WHERE id = :id",
                           star=round(statement[0]["avg(rating)"], 1), id=studysessionid)

        return redirect("/")
    else:
        return redirect("/")


@app.route("/mysessions")
@login_required
def mysessions():
    sessions = []
    links = []

    # Fetches all active and inactive studysessions from the database
    stmt = db.execute("SELECT * FROM studysessions WHERE userid = :userid",
                      userid=session["user_id"])

    return render_template("mysessions.html", sessions=stmt)


@app.route("/activesessions")
@login_required
def activesessions():
    sessions = []

    # Fetches all active study sessions from the database
    stmt = db.execute("SELECT * FROM studysessions WHERE isactive = :value",
                      value=1)
    return render_template("activesessions.html", sessions=stmt)


@app.route("/sessionpage")
@login_required
def sessionpage():
    # Retrives the id of the study session from the link
    id = request.args.get("id", None)

    # Select study sessions from the database where the id equals id retrieved from the link
    stmt = db.execute("SELECT * FROM studysessions WHERE id = :id",
                      id=id)

    # Select username from "users" the database where the id equals id retrieved from the link
    createdby = db.execute("SELECT username FROM users WHERE id = :id",
                           id=stmt[0]["userid"])

    # Selects reviews from the database that are associated with the studysession
    reviews = db.execute("SELECT * FROM ratings WHERE studysessionid = :id ORDER BY timestamp DESC",
                         id=id)
    return render_template("sessionpage.html", sessions=stmt, reviews=reviews, sp_id=id, createdby=createdby)


@app.route("/deactivate")
@login_required
def deactivate():
    # Retrives the id of the study session from the link
    id = request.args.get("id", None)

    # Changes active status to false
    stmt = db.execute("UPDATE studysessions SET isactive = :value WHERE id = :id",
                      value=0, id=id)
    return redirect("/")


@app.route("/editsession", methods=["GET", "POST"])
@login_required
def editsession():
    # Checks if data was posted, else loads form
    if request.method == "POST":

        # Retrieves user input from form
        id = request.form.get("sp_id")
        name = request.form.get("name")
        description = request.form.get("description")
        building = request.form.get("building")
        city = request.form.get("city")
        state = request.form.get("state")

        # Creates a string out of location input from user
        location = building.strip() + ", " + city.strip() + ", " + state.strip()

        # Update study session in database
        stmt1 = db.execute("UPDATE studysessions SET description = :description, building = :building, location = :location, userid = :userid WHERE id = :id",
                           description=description, building=building, location=location, userid=session["user_id"], id=id)
        return redirect("/")
    else:

         # Retrives the id of the study session from the link
        id = request.args.get("id", None)

        # Selects studysession from database
        stmt = db.execute("SELECT * FROM studysessions WHERE id = :id",
                          id=id)
        return render_template("edit.html", sessions=stmt, sp_id=id)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

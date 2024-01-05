import sqlite3

from flask import Flask, flash, redirect, render_template, request, session 
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import get_db_connection, signin_required

# Configure application
app = Flask(__name__) 

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@signin_required
def index():
    conn = get_db_connection()
    orders = conn.execute(
        "SELECT * FROM orders JOIN clients ON orders.client_id = clients.client_id JOIN inventory ON inventory.user_id = orders.user_id WHERE orders.user_id = 1"
    ).fetchall()
    conn.close()
    return render_template("index.html", orders=orders)


@app.route("/clients")
def clients():
    return render_template("clients.html")


@app.route("/inventory")
def inventory():
    return render_template("inventory.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign user in"""

    # Forget any user_id
    session.clear()

    # Define the return data object
    return_data = {
        "username": "",
        "password": ""
    }

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store form details in variables
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Username field is required.", "error")

        # Ensure password was submitted
        elif not password:
            flash("Password field is required.", "error")

        # Get db connection
        conn = get_db_connection()

        # Query database for username
        cur = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchall()

        # Close connection
        conn.close()

        # Ensure username exists 
        if len(cur) != 1:
            flash("User does not exist.", "error")
            return render_template("signin.html", data=return_data)
        
        # Ensure password is correct
        elif not check_password_hash(
            cur[0]["password"], password
        ):
            flash("Incorrect password.", "error")
            return_data["username"] = username
            return render_template("signin.html", data=return_data)

        # Remember which user has signed in
        session["user_id"] = cur[0]["user_id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clickig a link or via redirect)
    else:
        return render_template("signin.html", data=return_data)


@app.route("/signout")
def signout():
    """Sign out the current user."""

    # Forget any user_id
    session.clear()

    # Redirect user to signin page
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign user up"""

    # Forget any user_id
    session.clear()

    # Define the return data object
    return_data = {
        "email": "",
        "username": "",
        "password": "",
    }

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store form details in variables
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Get db connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Query database for username
        is_existinguser = cur.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchall()

        # Flash error if username already exists
        if len(is_existinguser) > 0:
            flash("Username, '{}' already exists.".format(username), "error")
            if email:
                return_data["email"] = email
            return render_template("signup.html", data=return_data)
        
        # Flash error if email, username, password or confirmation is blank
        elif not email or not username or not password or not confirmation:
            flash("All fields must be filled out.", "error")
            if email:
                return_data["email"] = email
            if username:
                return_data["username"] = username
            return render_template("signup.html", data=return_data)

        # Flash error if passwords do not match
        elif password != confirmation:
            flash("Passwords do not match.", "error")
            if email:
                return_data["email"] = email
            if username:
                return_data["username"] = username
            if password:
                return_data["password"] = password
            return render_template("signup.html", data=return_data)

        # If all details are correct, complete sign up and commit transaction
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password))
        )
        conn.commit()

        new_user = cur.execute(
            "SELECT user_id FROM users WHERE username = ?",
            (username,)
        ).fetchone()[0]

        # Set cookie if successful
        if new_user:
            session["user_id"] = new_user

        # Close connection
        conn.close()

        print(new_user)

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a lin or via redirect)
    else:
        return render_template("signup.html", data=return_data)


if __name__ == "__main__":
    app.run(debug=True)
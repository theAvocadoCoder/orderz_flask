import sqlite3

from flask import redirect, session
from functools import wraps

def get_db_connection():
    # Configure database connection
    conn = sqlite3.connect('orderz.db')
    conn.row_factory = sqlite3.Row
    return conn

def signin_required(f):
    # Decorator to require that a user is signed in.  If the user isn't, redirect them to the signin page.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    
    return decorated_function
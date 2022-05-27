"""Handles login and logout."""

import functools
from timeit import repeat
from flask import g
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import flash
from passlib.hash import sha512_crypt
from src.app import app, db
from src import sql

def require_login():
    """Check that user is logged in when accessing app."""

    def decorator(func):
        """Check access decorator."""

        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            """Check that user is logged in."""

            if  not g.user:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def hash_passwd(password) -> str:
    """Return password hash as string."""

    return sha512_crypt.hash(password)

def validate_passwd(user, password) -> bool:
    """Validate user's password."""

    return user and password and sha512_crypt.verify(password, user.password)

@app.before_request
def before_request():
    """Entry function to define g.user."""

    g.user = session.get('user')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Log in to the app."""

    if g.user:
        return redirect(url_for('home'))
    
    # Create new login
    invalidate_login()
    name = request.values.get('username')
    password = request.values.get('password')
    if name and password:
        user = sql.Users.query.filter_by(name = name).one_or_none()
        # If user doesn't exist, redirect to register page
        if not user:
            return redirect(url_for('register'))
        # If login succesful, set session user
        if validate_passwd(user, password):
            session['user'] = user.name
            return redirect(url_for('home'))
        # Flash error message if login unsuccessful
        flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Register a new user."""

    if g.user:
        return redirect(url_for('/'))
    
    # Create new user
    invalidate_login()
    name = request.values.get('username')
    password = request.values.get('password')
    repeat_pw = request.values.get('repeat_pw')
    if name and password and repeat_pw:
        # Repeated password not matching
        if password != repeat_pw:
            flash('Please enter matching passwords!')
            return render_template('register.html')
        # User already exists
        if name == sql.Users.query.filter_by(name = name).one_or_none():
            flash('Username already exists.')
            return render_template('register.html')
        # Successful creation of new user
        password = hash_passwd(password)
        print(password)
        db.session.add(sql.Users(name = name, password = password))
        db.session.commit()
        flash(f'User {name} has been successfully created.')
        return redirect(url_for('login'))
    return render_template('register.html')

def invalidate_login():
    """Remove all current user information from session."""

    session.pop('user', None)
    g.user = None

@app.route('/logout')
def logout():
    """Log out from the app."""

    invalidate_login()
    return redirect(url_for('home'))

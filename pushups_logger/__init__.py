from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import psycopg2
# db = SQLAlchemy()
from flask_login import LoginManager
import secrets
from .models import User
from .models import get_user_by_id

def create_app():
    app = Flask(__name__)
    
    app.secret_key = secrets.token_hex(16)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
       print("INIT===========",user_id)
       return get_user_by_id(user_id)
    
    from.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app

# if __name__ == '__main__':
#     # Run the app in debug mode if executed directly
#     create_app(debug=True).run()


# udaibhanu@MacBook-Air-4 Python % export FLASK_APP=PushUpApp
# udaibhanu@MacBook-Air-4 Python % flask run 




#@CONCEPT OF flask login


# Certainly! Let's go through a more detailed example with code to illustrate how Flask-Login uses the `user_id` stored in the session to load the user object for each request. This example will include parts of a Flask application setup, user login, and the user loader function.

# ### Step 1: Define the User Model

# First, we need a user model. For simplicity, let's assume we have a `User` class that represents users in our application.

# ```python
# class User:
#     def __init__(self, id, username):
#         self.id = id
#         self.username = username

# # Example users database
# users_db = {1: User(1, "Alice"), 2: User(2, "Bob")}
# ```

# ### Step 2: Setup Flask Application and Flask-Login

# Next, we set up the Flask application and configure Flask-Login, including defining the user loader function.

# ```python
# from flask import Flask, session, redirect, url_for, request
# from flask_login import LoginManager, login_user, login_required, logout_user

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     print("Loading user with ID:", user_id)
#     return users_db.get(int(user_id))
# ```

# ### Step 3: Define Login and Logout Views

# Now, let's define views for logging in and logging out. For simplicity, the login view simulates a login process without checking a password.

# ```python
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         user = users_db.get(int(user_id))
#         if user:
#             login_user(user)
#             return redirect(url_for('protected'))
#     return '''
#     <form method="post">
#         User ID: <input type="text" name="user_id"><br>
#         <input type="submit" value="Login">
#     </form>
#     '''

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
# ```

# ### Step 4: Define a Protected Route

# This is an example of a protected route that requires the user to be logged in.

# ```python
# @app.route('/protected')
# @login_required
# def protected():
#     return 'Logged in as: ' + session['_user_id']
# ```

# ### How It Works

# 1. **User Visits Login Page**: The user goes to `/login` and submits their user ID (for this example, let's say `1` for Alice).

# 2. **Login Process**: The `login` view function retrieves the user object from `users_db` using the submitted `user_id`, then calls `login_user(user)`, which stores the user's ID in the session.

# 3. **User Loader Callback**: For each subsequent request, Flask-Login retrieves the `user_id` from the session and calls `load_user(user_id)`. This function fetches the user object from `users_db` and returns it.

# 4. **Access Protected Route**: When the user navigates to `/protected`, Flask-Login checks if the user is logged in (by using the user loader to get the user object). Since the user is logged in, the view returns the message showing the user's ID.

# ### Summary

# This example demonstrates how Flask-Login manages user sessions. The `user_id` is stored in the session when `login_user(user)` is called. For each request, Flask-Login retrieves this `user_id` and uses the user loader function (`load_user`) to get the user object, which is then used to handle login-required routes and other user-specific tasks.

# Let me know if you have any questions or need further clarification!














# Certainly! Let's dive deeper into how the user loader callback works in Flask-Login, focusing on the process of retrieving the `user_id` from the session and using it to fetch the user object.

# ### Understanding Sessions

# In web applications, a session provides a way to store information (in variables) to be used across multiple pages. Flask, like many web frameworks, supports sessions that allow you to store information specific to a user from one request to the next. This is achieved by using a secure cookie that stores a session ID linked to server-side session data.

# ### Flask-Login and Sessions

# Flask-Login uses the session mechanism provided by Flask to store the ID of the logged-in user. When you log in a user with Flask-Login's `login_user(user)` function, Flask-Login stores the user's ID in Flask's session under the key `_user_id`. This is how Flask-Login keeps track of which user is logged in.

# ### The User Loader Callback

# The user loader callback is a function that you define and then tell Flask-Login about, using the `@login_manager.user_loader` decorator. Flask-Login calls this function whenever it needs to retrieve a user object for the current user. This typically happens at the beginning of each request, after the user has logged in.

# Here's the process in detail:

# 1. **Retrieving `user_id` from the Session**: At the start of a new request, Flask-Login looks for the `_user_id` in the session. This ID was stored there when the user logged in. Flask automatically loads the session at the beginning of each request, so Flask-Login can access the session data easily.

# 2. **Calling the User Loader Callback**: Flask-Login takes the `user_id` it found in the session and passes it to the user loader callback function. This function is responsible for taking that `user_id` and returning the corresponding user object. If the function returns a user object, Flask-Login considers the user as logged in for the duration of the request. If the function returns `None`, Flask-Login considers the user as not logged in.

# 3. **Fetching the User Object**: Inside the user loader callback, you typically perform a database lookup to retrieve the user. The `user_id` is used to find the specific user in your database. Once found, you create and return a user object that represents the logged-in user.

# ### Example User Loader Callback

# ```python
# @login_manager.user_loader
# def load_user(user_id):
#     # Assuming users_db is a dictionary mapping user IDs to user objects
#     return users_db.get(int(user_id))
# ```

# In this example, `users_db.get(int(user_id))` attempts to find the user in a hypothetical database (or in this case, a simple dictionary for demonstration purposes) using the `user_id`. If the user exists, the user object is returned. Flask-Login then uses this object for various user-related tasks during the request, such as checking permissions or displaying user-specific information.

# ### Summary

# The user loader callback is a crucial part of integrating Flask-Login into your application. It bridges the gap between Flask-Login's session management (which tracks the logged-in user by their ID) and your application's user model (which defines what a user is). By implementing this callback, you enable Flask-Login to load the current user's object at the beginning of each request, allowing you to build a personalized, user-aware web application.

# If you have any more questions or need further explanations, feel free to ask!
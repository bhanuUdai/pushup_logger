from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import get_db_connection, close_db_connection
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .models import User


auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['Post'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # we dont need to close  db connection while using with
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT email FROM users WHERE email = %s',(email,))
            # cur.execute(f"SELECT email FFROM users WHERE email = '{email}'")
            existing_user = cur.fetchone()
            if existing_user:
                print('User already exists')
            else:
                hashed_password = generate_password_hash(password)
                cur.execute('INSERT INTO users (email, name, password) VALUES (%s, %s, %s)', (email, name, hashed_password))
                
                # no need to commit while using with because the __exit__ method of the context manager do it .
                # conn.commit()
                
            #     hashed_password = generate_password_hash(password)
            #     curr.execute('INSERT INTO users (email ,name, password) VALUES(%s, %s, %s)', (email, name, hashed_password))
            # close_db_connection(conn, cur)
            
                print(email,name,password)
                return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods =['Post'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
          cur.execute(f"SELECT email FROM users WHERE email = '{email}'")
          user = cur.fetchone()
          if user:
              cur.execute(f"SELECT id, email, password, name FROM users WHERE email = '{email}'")
              user_data = cur.fetchone()
              print("user_data",user_data)
              
              user = User(user_data[0], user_data[1], user_data[2],  user_data[3])
              
              if isinstance(user_data[2], tuple):
                print("hashhh",user_data[2][0])
              hash_pass = user_data[2]
              print("hash_pass==>",hash_pass)
              method, salt, hash_val = hash_pass.split("$", 2)
              print("method, salt, hash_val",method, salt, hash_val)
              if check_password_hash(f"{method}${salt}${hash_val}", password):
                  print('Password is correct')
                  login_user(user, remember=remember)
                  return redirect(url_for('main.profile'))
              else:
                  print('Password is incorrect')
                  return redirect(url_for('auth.login'))
    
    
    
    # print(email,password)
    # return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')
    # return redirect(url_for('auth.login'))
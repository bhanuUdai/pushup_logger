from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import psycopg2
# db = SQLAlchemy()
from flask_login import LoginManager
import secrets
from pushups_logger.models import User
from pushups_logger.models import get_user_by_id

def create_app():
    app = Flask(__name__, template_folder = 'pushups_logger/templates')
    
    app.secret_key = secrets.token_hex(16)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
       print("INIT===========",user_id)
       return get_user_by_id(user_id)
    
    from pushups_logger.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from pushups_logger.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app


# from pushups_logger import create_app 
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode if executed directly
   app.run(debug=True)
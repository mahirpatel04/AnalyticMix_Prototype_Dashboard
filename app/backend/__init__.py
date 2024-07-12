from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin


db = SQLAlchemy()
DB_NAME = 'database.db'
admin = Admin()
def create_app():
    app = Flask(__name__)
    app.template_folder = "../frontend/templates"
    app.static_folder = "../frontend/static"
    app.config['SECRET_KEY'] = 'awe9ipurhfadakcjvadfjhkasdfsdljfw0984520493235oiia8sdlakjsr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    # admin.init_app(app)
    from .views import analytics, upload, auth
    from .views.main.routes import main
    
    app.register_blueprint(main)
    app.register_blueprint(analytics)
    app.register_blueprint(auth)
    app.register_blueprint(upload)
    
    from .models import User, CSV
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'pages.auth.auth.login'
    login_manager.login_message = ''
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
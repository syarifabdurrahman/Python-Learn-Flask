from flask import Flask

def create_app():
    app = Flask(__name__,template_folder='templates')

     # this for encript or secure cookies and session data related to our website
    app.config['SECRET_KEY']='this is secret key'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app


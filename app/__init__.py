from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import views
    from .controllers import controllers
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')

    return app
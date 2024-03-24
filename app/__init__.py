# app/__init__.py

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    if test_config:
        # load the test config if passed in
        app.config.update(test_config)
    else:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        import os
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says welcome
    @app.route('/welcome')
    def welcome():
        return 'Welcome to the Currency Exchange Service!'

    from .routes.currency import bp as currency_bp
    app.register_blueprint(currency_bp)

    return app

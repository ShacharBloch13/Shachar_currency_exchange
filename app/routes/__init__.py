# app/routes/__init__.py

from flask import Blueprint

# Import Blueprints from individual route modules
from .currency import bp as currency_bp


# Function to register all your Blueprints to the app
# This function can then be called from your app factory
def init_app(app):
    app.register_blueprint(currency_bp)

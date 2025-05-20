#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Union, Dict

app = Flask(__name__)


class Config:
    """App configuration for Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)

# Mock user "database"
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Get user by ID from login_as query parameter"""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set user in Flask global g before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match locale using:
       1. URL parameters
       2. User settings
       3. Request header
       4. Default locale
    """
    # 1. URL parameter
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    # 2. User setting
    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # 3. Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render index page"""
    return render_template('6-index.html')

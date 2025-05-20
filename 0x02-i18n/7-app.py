#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
from typing import Union, Dict
from datetime import datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)


class Config:
    """Babel config"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieve a user dictionary by login_as ID"""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Executed before each request to set g.user"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match locale"""
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine best match timezone"""
    tz_param = request.args.get('timezone')
    if tz_param:
        try:
            return pytz.timezone(tz_param).zone
        except UnknownTimeZoneError:
            pass

    if g.get('user'):
        tz_user = g.user.get('timezone')
        if tz_user:
            try:
                return pytz.timezone(tz_user).zone
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Render homepage with localized time"""
    current_time = format_datetime(datetime.now(), locale=get_locale())
    return render_template('index.html', current_time=current_time)

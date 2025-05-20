#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """App configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Select best-matching language"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render translated homepage"""
    return render_template('3-index.html')

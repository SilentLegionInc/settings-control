from flask import Flask, request, redirect, url_for, jsonify, render_template, flash
from flask_cors import CORS
from flask_login import LoginManager, login_manager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from src.logger import Logger
from src.settings_service import SettingsService

import os


# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)
# Setting env variables
os.environ['settings_login'] = SettingsService().config['login']
os.environ['settings_password'] = bcrypt.generate_password_hash(SettingsService().config['password']).decode('utf-8')

os.environ['settings_secret'] = SettingsService().config['secret']
app.secret_key = os.environ.get('settings_secret')

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../session.db'
db = SQLAlchemy(app)

# Here routes starts.
import src.routes

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from src.logger import Logger
from src.settings_service import SettingsService


# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SettingsService().server_config['secret']
app.config['USER_AUTH_HASH'] = SettingsService().server_config['authorization']
app.secret_key = SettingsService().server_config['secret']

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

# Here routes starts.
import src.routes

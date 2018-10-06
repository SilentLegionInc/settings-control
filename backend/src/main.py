from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from settings_service import SettingsService


# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SettingsService().private_server_config['secret']
app.secret_key = app.config['SECRET_KEY']
# app.config['USER_AUTH_HASH'] = SettingsService().server_config['authorization']

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

# Here routes starts.
import routes
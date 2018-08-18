from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from src.logger import Logger
from src.settings import Settings
import os

env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates/")),
    autoescape=select_autoescape(['html'])
)

app = Flask(__name__)
CORS(app)


@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return jsonify(Settings().load_current_server_config())
    elif request.method == 'POST':
        return jsonify(Settings().save_server_config(request.get_json()))


@app.route('/config', methods=['GET', 'POST'])
def ui_config():
    if request.method == 'GET':
        return env.get_template('config.html').render(config=Settings().load_current_server_config())
    elif request.method == 'POST':
        result = Settings().load_current_server_config()
        for key in request.form:
            result[key] = request.form.get(key)
        if Settings().save_server_config(result)['code'] == 0:
            Logger().info_message('Saved')
        else:
            Logger().info_message('Error')
        return env.get_template('config.html').render(config=Settings().load_current_server_config())




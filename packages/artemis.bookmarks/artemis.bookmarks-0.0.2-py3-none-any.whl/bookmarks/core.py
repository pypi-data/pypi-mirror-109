import os

import toml
from flask import Flask

from bookmarks.config import get_config_path

app = Flask(__name__)
app.config.root_path = os.getcwd()
config_path = get_config_path()
if config_path is not None:
	app.config.from_file(config_path, load=toml.load)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

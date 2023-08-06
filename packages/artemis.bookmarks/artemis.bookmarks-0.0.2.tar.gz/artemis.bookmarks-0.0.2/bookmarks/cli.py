from .core import app
from .db import db


@app.cli.command('db:init')
def init_db():
	db.create_all()

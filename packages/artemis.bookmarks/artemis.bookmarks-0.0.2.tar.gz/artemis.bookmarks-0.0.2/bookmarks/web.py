from flask import render_template

from .core import app


@app.route("/")
@app.route("/<name>")
def homepage(name=None):
	return render_template('homepage.html', name=name)

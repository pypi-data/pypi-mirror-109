from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .core import app

db = SQLAlchemy(app)

tags = db.Table(
	'tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
	db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'), primary_key=True),
)


class Bookmark(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.String, unique=True, nullable=False)
	label = db.Column(db.String(255))
	bookmarking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	category = db.relationship('Category', backref=db.backref('bookmarks', lazy=True))

	tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('bookmarks', lazy=True))

	def __repr__(self):
		return f'<Bookmark: {self.label if len(self.label) > 0 else self.link}>'


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	namePath = db.Column(db.String, unique=True)  # separator is /, doesn't start or end with one

	def __repr__(self):
		return f'<Category: {self.namePath}>'


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.String(64), unique=True)

	def __repr__(self):
		return f'<Tag: #{self.value}>'

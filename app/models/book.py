from ..extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)  # renamed from authors
    genre = db.Column(db.String(128), nullable=True)    # added
    year_published = db.Column(db.Integer, nullable=True)  # renamed from published_year
    summary = db.Column(db.Text, nullable=True)
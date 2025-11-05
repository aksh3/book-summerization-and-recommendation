from ..extensions import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)  # renamed from content
    rating = db.Column(db.Integer, nullable=False)
    book = db.relationship("Book", backref="reviews")
    user = db.relationship("User", backref="reviews")
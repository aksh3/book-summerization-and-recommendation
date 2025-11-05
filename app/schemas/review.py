from ..extensions import ma
from ..models.review import Review

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
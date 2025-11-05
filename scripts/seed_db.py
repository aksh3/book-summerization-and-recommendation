import os
from app.main import create_app
from app.extensions import db
from app.models.user import Role

def seed():
    app = create_app()
    with app.app_context():
        if not Role.query.filter_by(name="admin").first():
            db.session.add(Role(name="admin"))
        if not Role.query.filter_by(name="user").first():
            db.session.add(Role(name="user"))
        db.session.commit()
        print("Roles seeded.")

if __name__ == "__main__":
    seed()
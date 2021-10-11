from flaskblog import create_app, db
from flaskblog.models import User, Post #This is important for creation of fully developed Database
app = create_app()

db.init_app(app)

with app.app_context():
    db.create_all()
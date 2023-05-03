from . import db, create_app
app = create_app()
with app.app_context():
    db.create_all() # pass the create_app result so Flask-SQLAlchemy gets the configuration.
print(1)
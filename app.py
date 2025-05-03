from flask import Flask
from db import db
import models  # Імпортуємо, щоб SQLAlchemy бачив моделі
from models.tag import TagModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


@app.route("/")
def home():
    return {"message": "API працює"}


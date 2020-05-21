import os

from flask import Flask, render_template, request

# Import table definitions.
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)


### CREATE


@app.route("/api/create/team", methods=["POST"])
def createTeam():
    if request.method == "POST":
        name = request.form.get("name", "")

        new = Team(name)
        db.session.add(new)
        db.session.commit()
        return new.json(), 201


@app.route("/api/create/person", methods=["POST"])
def createPerson():
    if request.method == "POST":
        # form
        name = request.form.get("name", "")
        teamId = request.form.get("teamId", "")
        email = request.form.get("email", "")
        contact = request.form.get("contact", "")

        # json
        # name = request.json["name"]
        # teamId = request.json["teamId"]
        # email = request.json["email"]
        # contact = request.json["contact"]

        new = Person(name, teamId, email, contact)
        db.session.add(new)
        db.session.commit()
        return new.json(), 201


### READ


@app.route("/api/team", methods=["GET"])
def readAllTeam():
    if request.method == "GET":
        teams = Team.query.all()
        people = Person.query.all()

        return render_template("index.html", teams=teams, people=people)


def main():
    # Create tables based on each table definition in `models`
    db.create_all()


if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()

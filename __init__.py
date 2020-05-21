import time
import logging as logger

from flask import Flask, request

from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logger.basicConfig(level="DEBUG")

# instantiate flask app
app = Flask(__name__)

# instantiate sqlalchemy engine
engine = create_engine("sqlite:///lunchBreak.db", echo=False)
# create a session
session = sessionmaker(bind=engine)()
# declarative base
Base = declarative_base()


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name.strip()

    def __str__(self):
        return f"{self.id} - {self.name}"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Person(Base):

    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    teamId = Column(Integer, ForeignKey("team.id"))
    email = Column(String(100))
    contact = Column(String(20))
    onLunchBreak = Column(Boolean)
    started = Column(Integer)

    def __init__(self, name: str, teamId: int, email: str = "", contact: str = ""):
        self.name = name
        self.teamId = teamId
        self.email = email
        self.contact = contact
        self.onLunchBreak = False
        self.started = None

    def __str__(self):
        return f"{self.name} ({self.email})"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "teamId": self.teamId,
            "email": self.email,
            "contact": self.contact,
            "onLunchBreak": self.onLunchBreak,
            "started": self.started,
        }


### CREATE


@app.route("/api/create/team/", methods=["POST"])
def createTeam():
    if request.method == "POST":
        # session = sessionmaker(bind=engine)()
        name = request.json["name"]

        new = Team(name)
        session.add(new)
        session.commit()
        return new.json(), 201


@app.route("/api/create/person/", methods=["POST"])
def createPerson():
    if request.method == "POST":
        # session = sessionmaker(bind=engine)()
        name = request.json["name"]
        teamId = request.json["teamId"]
        email = request.json["email"]
        contact = request.json["contact"]

        new = Person(name, teamId, email, contact)
        session.add(new)
        session.commit()
        return new.json(), 201


### READ


@app.route("/api/team/", methods=["GET"])
def readAllTeam():
    if request.method == "GET":
        teams = session.query(Team).all()
        # TODO: jsonify
        data = dict()
        for team in teams:
            data[team.id] = team.json()
        return data, 200


@app.route("/api/person/", methods=["GET"])
def readAllPerson():
    if request.method == "GET":
        people = session.query(Person).all()
        # TODO: jsonify
        data = dict()
        for person in people:
            data[person.id] = person.json()
        return data, 200


### READ, UPDATE, DELETE


@app.route("/api/team/<id>", methods=["GET", "POST", "DELETE"])
def teamById(id):
    if request.method == "GET":
        exist = session.query(Team).filter(Team.id == id).count()
        if exist:
            people_working = (
                session.query(Person)
                .filter(Person.teamId == id)
                .filter(Person.onLunchBreak == False)
            )
            people_lb = (
                session.query(Person)
                .filter(Person.teamId == id)
                .filter(Person.onLunchBreak == True)
            )

            return {"people_working": people_working, "people_lb": people_lb}, 200
        else:
            return {"msg": "Team Not Found"}, 404

    elif request.method == "POST":
        exist = session.query(Team).filter(Team.id == id).count()
        if exist:
            name = request.json["name"]
            team = session.query(Team).filter(Team.id == id).first()
            team.name = name
            return team.json(), 200
        else:
            return {"msg": "Team Not Found"}, 404

    elif request.method == "DELETE":
        exist = session.query(Team).filter(Team.id == id).count()
        isEmptyTeam = (
            True
            if session.query(Person).filter(Person.teamId == id).count() == 0
            else False
        )
        if exist:
            if isEmptyTeam:
                session.query(Team).filter(Team.id == id).delete()
                return {"msg": "Team Deleted"}, 200
            else:
                return {"msg": "Delete Team with memeber not allowed"}, 403
        else:
            return {"msg": "Team Not Found"}, 404


@app.route("/api/person/<id>/", methods=["GET", "POST", "DELETE"])
def personById(id):
    if request.method == "GET":
        exist = session.query(Person).filter(Person.id == id).count()
        if exist:
            person = session.query(Person).filter(Person.id == id).first()
            return person.json(), 200
        else:
            return {"msg": "Person Not Found"}, 404

    elif request.method == "POST":

        # get a timestamp
        started = time.time()

        try:
            name = request.json["name"]
            teamId = request.json["teamId"]
            email = request.json["email"]
            contact = request.json["contact"]
            onLunchBreak = request.json["onLunchBreak"]
        except:
            return {"data": "Key Error"}, 400

        exist = session.query(Person).filter(Person.id == id).count()
        if exist:
            person = session.query(Person).filter(Person.id == id).first()

            person.name = name
            person.teamId = teamId
            person.email = email
            person.contact = contact
            person.onLunchBreak = onLunchBreak
            person.started = started if onLunchBreak else None

            return person.json(), 200

        else:
            return {"data": "Person Not Found"}, 404

    elif request.method == "DELETE":
        exist = session.query(Person).filter(Person.id == id).count()
        if exist:
            person = session.query(Person).filter(Person.id == id).delete()
        return {"msg": "Team Deleted"}, 200


if __name__ == "__main__":

    from os import path

    if not path.exists("lunchBreak.db"):
        # CREATE TABLE
        Base.metadata.create_all(engine)

        # Create some data
        t1 = Team("SAP Machine Learning")
        t2 = Team("SAP Data Intelligence")
        session.add(t1)
        session.add(t2)

        p = Person("Sonali", 2, email="Sonali@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Naylin", 2, email="Naylin@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Smita", 2, email="Smita@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Shide", 2, email="Shide@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Nicola", 2, email="Nicola@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Navneet", 2, email="Navneet@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Thiru", 2, email="Thiru@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Leonard", 2, email="Leonard@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Victor", 2, email="Victor@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Srini", 2, email="Srini@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Arief", 2, email="Arief@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Srishti", 2, email="Srishti@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Daniel", 2, email="Daniel@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Suresh", 2, email="Suresh@gmail.com", contact="91234567")
        session.add(p)
        p = Person("Mark", 2, email="Mark@gmail.com", contact="91234567")
        session.add(p)
        session.commit()

    # log
    logger.debug("Starting Flask Server")

    # run app
    app.run(host="0.0.0.0", port=5000, debug=True)

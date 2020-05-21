from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name.strip()

    def __str__(self):
        return f"{self.id} - {self.name}"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Person(db.Model):

    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    teamId = db.Column(db.Integer, db.ForeignKey("team.id"))
    email = db.Column(db.String(100))
    contact = db.Column(db.String(20))
    onLunchBreak = db.Column(db.Boolean)
    started = db.Column(db.Integer)

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

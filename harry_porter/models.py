from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    year_enrolled = db.Column(db.Integer, nullable=False)
    classes = db.relationship('StudentClass', backref='student', lazy=True)
    quidditch_teams = db.relationship('StudentQuidditchTeam', backref='student', lazy=True)

class StudentClass(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), primary_key=True)

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    year_taught = db.Column(db.Integer, nullable=False)
    students = db.relationship('StudentClass', backref='class', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    classes = db.relationship('Class', backref='teacher', lazy=True)
    house_teacher = db.relationship('HouseTeacher', backref='teacher', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String, nullable=False)
    classes = db.relationship('Class', backref='subject', lazy=True)

class HouseTeacher(db.Model):
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), primary_key=True)
    year_commenced = db.Column(db.Integer, nullable=False)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_name = db.Column(db.String, nullable=False)
    founder_first_name = db.Column(db.String, nullable=False)
    founder_last_name = db.Column(db.String, nullable=False)
    primary_color = db.Column(db.String, nullable=False)
    secondary_color = db.Column(db.String, nullable=False)
    students = db.relationship('Student', backref='house', lazy=True)
    house_teachers = db.relationship('HouseTeacher', backref='house', lazy=True)
    house_points = db.relationship('HousePoints', backref='house', lazy=True)
    quidditch_teams = db.relationship('QuidditchTeam', backref='house', lazy=True)

class HousePoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_points = db.Column(db.Integer, nullable=False)

class QuidditchTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    team_year = db.Column(db.Integer, nullable=False)
    players = db.relationship('StudentQuidditchTeam', backref='quidditch_team', lazy=True)
    matches_team1 = db.relationship('Match', foreign_keys='Match.team1_id', backref='team1', lazy=True)
    matches_team2 = db.relationship('Match', foreign_keys='Match.team2_id', backref='team2', lazy=True)

class StudentQuidditchTeam(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    quidditch_team_id = db.Column(db.Integer, db.ForeignKey('quidditch_team.id'), primary_key=True)
    position = db.Column(db.String, nullable=False)
    is_captain = db.Column(db.Boolean, nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('quidditch_team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('quidditch_team.id'), nullable=False)
    team1_score = db.Column(db.Float, nullable=False)
    team2_score = db.Column(db.Float, nullable=False)
    date_played = db.Column(db.DateTime, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from typing import Self
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
   db.init_app(app)
   return db

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(255), nullable=False, unique=True)
    email_user = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    groupss = db.relationship('Group', secondary='user_group', back_populates='users')

    def set_password(self, password):
        # Generate a random salt
        salt = bcrypt.gensalt()

        # Hash the password using the salt and the bcrypt algorithm
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Store the salt and the hashed password in the database
        self.password_salt = salt.decode('utf-8')
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password):
        # Hash the password using the stored salt and the bcrypt algorithm
        password_hash = bcrypt.hashpw(password.encode('utf-8'), self.password_salt.encode('utf-8'))

        # Compare the hashed password to the stored password hash
        return password_hash == self.password_hash.encode('utf-8')
    
    
class Group(db.Model):
    id_group = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(255), nullable=False)
    # para hacer 1-n entre proyecto y encuesta
    topics = db.relationship('Topic', backref='group')
    users = db.relationship('User', secondary='user_group', back_populates='groups')

class Topic(db.Model):
    id_topic = db.Column(db.Integer, primary_key=True)
    title_topic = db.Column(db.String(255), nullable=False)
    owner_topic = db.Column(db.Integer, nullable=False)
    type_topic = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, default=False)
    participation = db.Column(db.Integer, nullable=False)
    answers = db.relationship('Topic_answer', backref='topic')
    tickets = db.relationship('Topic_ticket', backref='topic')

class Topic_answer(db.Model):
    id_topic_answer = db.Column(db.Integer, primary_key=True)
    id_topic = db.Column(db.Integer, nullable=False)
    id_order = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

class Topic_ticket(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id_topic'), primary_key=True)
    completed = db.Column(db.Boolean, default=False)

class Topic_item(db.Model):
    id_topic_item = db.Column(db.Integer, primary_key=True)
    id_topic = db.Column(db.Integer, nullable=False)
    id_order = db.Column(db.Integer, nullable=False)
    text_answers = db.Column(db.String(255), nullable=False)

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id_user'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id_group'), primary_key=True) )


user_topic = db.Table('user_topic',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id_topic'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id_user'), primary_key=True) )
 


#class Stats:
    #projects = Project
    #surveys = Survey
    #survey = Survey
    #selected_project: int
    #selected_survey: int
    #survey_has_answers: int
    

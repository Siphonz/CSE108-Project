#Database table for trivia
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(UserMixin, db.Model):
    #Users can be regular players or administrators.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    #False for players. True for admin
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


class Category(db.Model):
    #Topics
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Question(db.Model):
    # Each question belongs to one category
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    #The question itself and its four answer choices.
    question_text = db.Column(db.String(300), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False, default="easy")
    option_a = db.Column(db.String(150), nullable=False)
    option_b = db.Column(db.String(150), nullable=False)
    option_c = db.Column(db.String(150), nullable=False)
    option_d = db.Column(db.String(150), nullable=False)

    #Store only the correct letter: A, B, C, or D.
    correct_answer = db.Column(db.String(1), nullable=False)

    #Lets templates use question.category.name.
    category = db.relationship("Category")


class Attempt(db.Model):
    #One Attempt is one completed quiz by one player.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Lets templates use attempt.user.username and attempt.category.name.
    user = db.relationship("User")
    category = db.relationship("Category")

from app import db, login, whooshee
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def jsonify(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

    def __repr__(self):
        return f'<User {self.username}>'

@whooshee.register_model('name')
class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    meal = db.Column(db.String(32))
    cuisine = db.Column(db.String(32))
    vegetarian = db.Column(db.Boolean())
    vegan = db.Column(db.Boolean())
    difficulty_rating = db.Column(db.Integer())
    taste_rating = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

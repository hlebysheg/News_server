from app import db, app
from datetime import datetime
from flask_login import LoginManager, UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key = True)
    disc = db.Column(db.String(300), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_name = db.Column(db.String(50), db.ForeignKey('users.username'), default="anon")
    def __repr__(self):
        return '<Article %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    article = relationship("Article",  backref="user", lazy=True)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.username)
    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password_hash, password)
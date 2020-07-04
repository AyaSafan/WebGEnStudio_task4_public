from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

db = SQLAlchemy()

# all classes inherit from db.Model. This allows for the class to have some built-in relationship with SQLAlchemy to interact with the database.
#__str__ is the built-in function in python, used in classes for string representation of object.

# -------------------    Users  ----------------------# #----1----#

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)
    username= db.Column(db.String, nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    address= db.Column(db.String, nullable = False)
  
    def __str__(self):
        return f"{self.username}"

     




from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class StudentModel(db.Model):  #model class name
    __tablename__='student'  

    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(),nullable=False)
    last_name=db.Column(db.String())
    email=db.Column(db.String())
    password=db.Column(db.String(10))
    gender=db.Column(db.String())

    def __init__(self,first_name,last_name,email,password,gender):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=password
        self.gender=gender

    def __repr__(self):
        return f'{self.first_name}:{self.last_name}'
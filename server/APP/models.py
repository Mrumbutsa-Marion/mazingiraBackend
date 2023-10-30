from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    User_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Password = db.Column(db.String)
    Role = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
#the relationships
    organizations = db.relationship('Organization', backref='user')
    donations = db.relationship('Donation', backref='donor')

class Organization(db.Model):
    __tablename__ = 'Organization'
    Organization_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('User.User_ID'))
    Name = db.Column(db.String)
    Description = db.Column(db.Text)
    Contact_Information = db.Column(db.String)
    Status = db.Column(db.String)
#the relatioships
    donations = db.relationship('Donation', backref='organization')
    stories = db.relationship('Story', backref='organization')
    beneficiaries = db.relationship('Beneficiary', backref='organization')

class Donation(db.Model):
    __tablename__ = 'Donation'
    Donation_ID = db.Column(db.Integer, primary_key=True)
    Donor_User_ID = db.Column(db.Integer, db.ForeignKey('User.User_ID'))
    Organization_ID = db.Column(db.Integer, db.ForeignKey('Organization.Organization_ID'))
    Amount = db.Column(db.Numeric)
    Donation_Type = db.Column(db.String)
    Anonymous = db.Column(db.Boolean)
    Date = db.Column(db.Date)

class Story(db.Model):
    __tablename__ = 'Story'
    Story_ID = db.Column(db.Integer, primary_key=True)
    Organization_ID = db.Column(db.Integer, db.ForeignKey('Organization.Organization_ID'))
    Title = db.Column(db.String)
    Content = db.Column(db.Text)
    Images = db.Column(db.String)
    Date_Created = db.Column(db.Date)

class Beneficiary(db.Model):
    __tablename__ = 'Beneficiary'
    Beneficiary_ID = db.Column(db.Integer, primary_key=True)
    Organization_ID = db.Column(db.Integer, db.ForeignKey('Organization.Organization_ID'))
    Name = db.Column(db.String)
    Description = db.Column(db.Text)
    Inventory_Received = db.Column(db.Text)
    inventory = db.relationship('Inventory', backref='beneficiary')

class Inventory(db.Model):
    __tablename__ = 'Inventory'
    Inventory_ID = db.Column(db.Integer, primary_key=True)
    Beneficiary_ID = db.Column(db.Integer, db.ForeignKey('Beneficiary.Beneficiary_ID'))
    Description = db.Column(db.String)
    Quantity = db.Column(db.Integer)
    Date_Received = db.Column(db.Date)
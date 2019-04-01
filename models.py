from flask_sqlalchemy import SQLAlchemy
  
db = SQLAlchemy()
  
groups_contacts = db.Table('groups_contacts',
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)
   
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    address = db.Column(db.String(80), nullable=True, unique=False)
    phone = db.Column(db.String(80), nullable=True, unique=True)
    groups = db.relationship('Group', secondary=groups_contacts, lazy='subquery',
        backref=db.backref('contacts', lazy=True))
        
    def __repr__(self):
        return 'Contact: %s' % self.full_name
  
    def to_dict(self):
        groups = []
        for g in self.groups:
            groups.append(g.not_dict())
        return { 
          "id": self.id, 
          "full_name": self.full_name,
          "email": self.email,
          "address": self.address,
          "phone": self.phone,
          "groups": groups
        }
        
    def not_dict(self):
        groups = []
        for g in self.groups:
            groups.append(g.id)
        return { 
          "id": self.id, 
          "full_name": self.full_name,
          "email": self.email,
          "address": self.address,
          "phone": self.phone,
          "groups": groups
        }
        
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
        
    def __repr__(self):
        return 'Group: %s' % self.name
  
    def to_dict(self):
        contacts = []
        for c in self.contacts:
            contacts.append(c.not_dict())
        return { 
          "id": self.id, 
          "name": self.name,
          "contacts": contacts 
        }
        
    def not_dict(self):
        contacts = []
        for c in self.contacts:
            contacts.append(c.id)
        return { 
            "id": self.id, 
            "name": self.name,
            "contacts": contacts 
            }
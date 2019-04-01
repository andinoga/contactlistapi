import os
import sqlalchemy
from sqlalchemy import desc
from models import db, Contact, Group, groups_contacts
from flask_migrate import Migrate
from flask import Flask, jsonify, request


app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/emssseeeaoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)

def no_response():
    no_response = jsonify({"error": 400, "message":"no member found" })
    no_response.status_code = 400
    return no_response

def getAll(table):
    entries = table.query.all()
    arr = []
    for e in entries:
        entry = e.not_dict()
        arr.append(entry)
    return arr

def getID(anID, table):
    if anID is not None:
        entry = table.query.get(anID)
        return jsonify({"data": entry.to_dict()})

    return(no_response())

def deleteOne(anID, table):
    if id is not None:
        entry = table.query.get(anID)
        arr = []
        arr.append(entry)
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"deleted": "%s" % arr})
    
    return(no_response())

def updateGroup(groupID, request):
    if groupID is not None:
        info = request.get_json() or {}
        group = Group.query.get(groupID)
        group.name = info["name"]
        db.session.commit() 
        return jsonify({"status_code":"200","data":group.not_dict()})
        
    return(no_response())

def updateContact(contactID, request):
    if contactID is not None:
        info = request.get_json() or {}    
        contact = Contact.query.get(contactID) 
        contact.full_name = info["full_name"] 
        contact.email = info["email"] 
        contact.address = info["address"] 
        contact.phone = info["phone"] 
        if info["groups"] is not None:
            for g in info["groups"]:
                group = Group.query.get(g)
                if group is not None:
                    contact.groups.append(group)
                else:
                    return jsonify("error")
        db.session.commit()
        return jsonify({"status_code":"200","data":contact.not_dict()})

    return(no_response())
    

@app.route('/', methods=['GET'])
def default(): 
    return("TEST")
    
@app.route('/groups', methods=['GET'])
def allGroups(): 
    return jsonify({"data": getAll(Group)})
    
@app.route('/contacts', methods=['GET'])
def allContacts(): 
    return jsonify({"data": getAll(Contact)})

@app.route('/group/<int:id>', methods=['GET','PUT','DELETE'])
def groupID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Group))
        elif request.method == 'PUT':
            return(updateGroup(id, request))
        elif request.method == 'DELETE':
            return(deleteOne(id, Group))
        else:
            return("NOTHING")

@app.route('/group/add', methods=['POST'])
def groupAdd(): 
    info = request.get_json() or {}
    group = Group(
        name=info["name"]
        )
    print(info["name"])
    db.session.add(group)
    db.session.commit()
    return jsonify({"response":"ok"})

@app.route('/contact/<int:id>', methods=['GET','PUT','DELETE'])
def contactID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Contact))
        elif request.method == 'PUT':
            return(updateContact(id, request))
        elif request.method == 'DELETE':
            return(deleteOne(id, Contact))
        else:
            return("NOTHING")

@app.route('/contact/add', methods=['POST'])
def contactAdd(): 
    info = request.get_json() or {}
    contact = Contact(
        full_name=info["full_name"],
        email = info["email"],
        address = info["address"],
        phone = info["phone"]
        )    
    if info["groups"] is not None:
        for g in info["groups"]:
            group = Group.query.get(g)
            if group is not None:
                contact.groups.append(group)
            else:
                return jsonify("error")
    
    db.session.add(contact)
    db.session.commit()
    return jsonify({"response":"ok"})
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
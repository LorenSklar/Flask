## FRAMEWORK
from flask import Flask, jsonify, request

app = Flask(__name__)

## DATABASE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


## DECORATORS
app = Flask(__name__)

@app.route("/")
@app.route("/puppies")
def puppiesFunction():
  method = request.args.get('method', 'GET')
  method = method.upper()
  pupid = request.args.get('pupid', '')
  name = request.args.get('name', None)
  description = request.args.get('description', None)

  if pupid == '':
    if method == 'GET':
  	  return getAllPuppies()

    elif method == 'POST':
      return makeNewPuppy(name, description)

    else:
  	  return error()

  else:
    if method == 'GET':
  	  return getPuppy(pupid)

    elif method == 'PUT':
  	  return updatePuppy(pupid, name, description)

    elif method == 'DELETE':
  	  return deletePuppy(pupid)

    else:
  	  return error()


def getAllPuppies():
  with app.app_context():
    puppies = session.query(Puppy).all()
    return jsonify(Puppies=[pup.serialize for pup in puppies])

def getPuppy(pupid):
  print ("Getting puppy with pupid %s" % pupid)
  puppy = session.query(Puppy).filter_by(pupid = pupid).one()
  return jsonify(puppy=puppy.serialize)

def makeNewPuppy(name, description):
  print ("Adding a new puppy to the family...")
  print ("Name:", name)
  print ("Description:", description)
  puppy = Puppy(name = name, description = description)
  session.add(puppy)
  session.commit()
  return jsonify(Puppy=puppy.serialize)

def updatePuppy(pupid, name, description):
  puppy = session.query(Puppy).filter_by(pupid = pupid).one()
  if name:
    puppy.name = name
  if description:
    puppy.description = description
  session.add(puppy)
  session.commit()
  return "Good to go! We updated puppy with pupid %s" % pupid

def deletePuppy(pupid):
  puppy = session.query(Puppy).filter_by(pupid = pupid).one()
  session.delete(puppy)
  session.commit()
  return "Sorry to see you go! We removed puppy with pupid %s" % pupid

def error():
  return "I'm not sure what you're asking."

from flask import Flask, request, jsonify, render_template, Response, send_from_directory, session
from flask_session import Session
from lib.db import dbconnect, db_create, School, User, Club, Message, Position, UserClubPositionMapping

import json
import logging
import os

app = Flask(__name__)


# config for Flask-Session
SESSION_TYPE = 'filesystem'
app.secret_key = '046b48a135cb6d14905c4bbd632bba23f4e56084877851e1bc2711d607a87d99'
app.config.from_object(__name__)
Session(app)

db_options = {'db_file': 'my.db'}

def get_or_create_school(session, school_name, address, email=None, phone=None):

    school = session.query(School).filter(School.address == address).one_or_none()
    if school:
        return school
    school = School(name=school_name, address=address, email = email, phone = phone)
    session.add(school)
    session.flush()
    return school

def get_or_create_position(session, admin_position):
    position = session.query(Position).filter(Position.position_type == admin_position).one_or_none()
    if position:
        return position.id
    position = Position(position_type = admin_position)
    session.add(position)
    session.flush()
    return position.id

@app.route('/user', methods=['GET'])
def get_user():

    username = request.args.get('username', "")
    
    Session, engine = dbconnect(db_options)
    session = Session()

    if username != "":
        users = session.query(User).filter(User.username == username).all()
    else:
        users = session.query(User).all()
        
    ret_users = []
    for u in users:
        ret_users.append(
            {
                'id': u.id,
                'username': u.username,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'school_id': u.school_id,
                'created_on': u.created_on,
            }
        )
        #users = map(lambda u: dict(u), users)
    return jsonify(ret_users)


@app.route('/user', methods=['POST'])
def create_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    user = User(
        first_name=j.get('first_name'),
        last_name=j.get('last_name'),
        username=j.get('username'),
        school_id=get_or_create_school(session, j.get('schoolName'), j.get('schoolAddress')).id,
        email=j.get('email')
    )

    session.add(user)
    session.commit()
    return jsonify(
        {
            'id': user.id
        }
    )


@app.route('/user', methods=['PUT'])
def modify_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    userID = j.get('id')
    matchingUser = session.query(User).filter(User.id == userID).one_or_none()
    if matchingUser:
        if j.get('first_name') != None:
            matchingUser.first_name=j.get('first_name')
        if j.get('last_name') != None:
            matchingUser.last_name=j.get('last_name')
        if j.get('username') != None:
            matchingUser.username=j.get('username')
        if j.get('school_id') != None:
            matchingUser.school_id=j.get('school_id')
        if j.get('email') != None:
            matchingUser.email=j.get('email')
        session.commit()
        return jsonify(
            {
                'id': matchingUser.id
            }
        )
    else:
        response = jsonify( {'message': 'User not found'} )
        response.status_code = 404
        return response


@app.route('/user', methods=['DELETE'])
def delete_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    userID = j.get('id')
    matchingUser = session.query(User).filter(User.id == userID).one_or_none()
    if matchingUser:
        session.delete(matchingUser)
        session.commit()
        return jsonify(
            {
                'id': matchingUser.id
            }
        )
    else:
        response = jsonify( {'message': 'User not found'} )
        response.status_code = 404
        return response


# query using school_id
@app.route('/club', methods=['GET'])
def get_club():

    schoolID = request.args.get('school_id')
    Session, engine = dbconnect(db_options)
    session = Session()
    clubs = session.query(Club).filter(Club.school_id == schoolID).all()
    ret_clubs = []
    for c in clubs:
        ret_clubs.append(
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'school_id': c.school_id,
                'category': c.category,
                'location': c.location,
                'usualTime': c.usualTime,
                'img_type': c.img_type
            }
        )

    response = jsonify(ret_clubs)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
 

@app.route('/club', methods=['POST'])
def create_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()

    club = Club(
        name=j.get('name'),
        school_id=j.get('school_id'),
        description=j.get('description'),
        category=j.get('category'),
        location=j.get('location'),
        usualTime=j.get('usualTime'),
        img_type=j.get('img_type', None)
    )
    session.add(club)
    session.commit()
    return jsonify(
        {
            'id': club.id
        }
    )


@app.route('/club', methods=['PUT'])
def modify_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    clubID = j.get('id')
    matchingClub = session.query(Club).filter(Club.id == clubID).one_or_none()
    if matchingClub:
        if j.get('name') != None:
            matchingClub.name=j.get('name')
        if j.get('school_id') != None:
            matchingClub.school_id=j.get('school_id')
        if j.get('description') != None:
            matchingClub.description=j.get('description')
        if j.get('category') != None:
            matchingClub.category=j.get('category')
        if j.get('location') != None:
            matchingClub.location=j.get('location')
        if j.get('usualTime') != None:
            matchingClub.usualTime=j.get('usualTime')
        if j.get('img_type') != None:
            matchingclub.img_type=j.get('img_type')

        session.commit()
        return jsonify(
            {
                'id': clubID
            }
        )
    else:
        response = jsonify( {'message': 'Club not found'} )
        response.status_code = 404
        return response

@app.route('/club', methods=['DELETE'])
def delete_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    clubID = j.get('id')
    matchingClub = session.query(Club).filter(Club.id == clubID).one_or_none()
    if matchingClub:
        session.delete(matchingClub)
        session.commit()
        return jsonify(
            {
                'id': clubID
            }
        )
    else:
        response = jsonify( {'message': 'Club not found'} )
        response.status_code = 404
        return response


@app.route('/schools', methods=['POST'])
def create_school():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    school_id = get_or_create_school(session, j['name'], j['address'], j['email'], j['phone']).id
    session.commit()
    return jsonify(
        {
            'id': school_id,
            'name': j.get('name'),
            'address': j.get('address'),
            'email': j.get('email'),
            'phone': j.get('phone')

        }
    )

@app.route('/schools', methods=['GET'])
def get_schools():
    Session, engine = dbconnect(db_options)
    session = Session()
    schools = session.query(School).all()
    app.logger.info(schools)
    formatted_schools = []
    for s in schools:
        formatted_schools.append({
            'id': s.id,
            'name': s.name,
            'address': s.address,
            'email': s.email,
            'phone': s.phone
        })
    response = Response(json.dumps(formatted_schools))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/message', methods=['POST'])
def create_message():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    message = Message(
        club_id=j.get('club_id'),
        message=j.get('message')
    )
    session.add(message)
    session.commit()
    return jsonify(
        {
            'id': message.id
        }
    )

@app.route('/message', methods=['GET'])
def get_message():
    club_id = request.args.get('club_id')
    Session, engine = dbconnect(db_options)
    session = Session()
    messages = session.query(Message).filter(Message.club_id == club_id).all()
    #print (messages)
    ret_messages = []
    for m in messages:
        ret_messages.append(
            {
                'id': m.id,
                'club_id': m.club_id,
                'message': m.message
            }
        )
    response = Response(json.dumps(ret_messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/position', methods=['POST'])
def create_position():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    position_id = get_or_create_position(session, j['position_type'])
    session.commit()
    return jsonify(
        {
            'id': position_id
        }
    )

@app.route('/position', methods=['GET'])
def get_positions():
    Session, engine = dbconnect(db_options)
    session = Session()
    positions = session.query(Position).all()
    app.logger.info(positions)
    formatted_positions = []
    for p in positions:
        formatted_positions.append({
            'position_type': p.position_type
        })
    response = Response(json.dumps(formatted_positions))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/adminuser', methods=['POST'])
def create_admin():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    admin = UserClubPositionMapping(
        user_id=j.get('user_id'),
        club_id=j.get('club_id'),
        position_id =j.get('position_id')
    )
    session.add(admin)
    session.commit()
    return jsonify(
        {
            'id': admin.id
        }
    )



@app.route('/adminuser', methods=['GET'])
def get_admins():
    Session, engine = dbconnect(db_options)
    session = Session()
    admins = session.query(UserClubPositionMapping).all()
    users = session.query(User).all()
    app.logger.info(admins)
    formatted_admins = []
    for a in admins:
        for u in users:
            if (a.user_id == u.user_id):
                formatted_admins.append({
                    'user_id': u.user_id,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'username': u.username,
                    'school_id': u.school_id,
                    'email': u.email
                })
    response = Response(json.dumps(formatted_admins))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    return send_from_directory(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'),
        'index.html'
    )


# Subscribing/unsubscribing user from club

@app.route('/subscriptions', methods=['GET'])
def subscriptions():    
    Session, engine = dbconnect(db_options)
    session = Session()

    subscriptions = session.query(UserClubPositionMapping).all()
    
    ret_subs = []
    for s in subscriptions:
        ret_subs.append(
            {
                'id': s.id,
                'user_id': s.user_id,
                'club_id': s.club_id,
                'position_id': s.position_id,
                'created_on': s.created_on,
            }
        )
        #users = map(lambda u: dict(u), users)
    return jsonify(ret_subs)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    link = UserClubPositionMapping(
        user_id=j.get('user_id'),
        club_id=j.get('club_id'),
        position_id=j.get('position_id')
    )

    session.add(link)
    session.commit()
    return jsonify(
        {
            'user_id': link.user_id,
            'club_id': link.club_id,
            'position_id': link.position_id
        }
    )

@app.route('/unsubscribe', methods=['DELETE'])
def unsubscribe():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    userID = j.get('user_id')
    clubID = j.get('club_id')
    # comma separated list of bool expr are AND
    matchingLink = session.query(UserClubPositionMapping).filter(UserClubPositionMapping.user_id == userID, UserClubPositionMapping.club_id == clubID).one_or_none()
    if not matchingLink:
        response = jsonify( {'message': 'Subscription between user ID and club ID not found'} )
        response.status_code = 202
        return response
    session.delete(matchingLink)
    session.commit()
    return jsonify(
        {
            'user_id': matchingLink.user_id,
            'club_id': matchingLink.club_id,
            'position_id': matchingLink.position_id
        }
    )


# Flask-Session routes

@app.route('/setLogin', methods=['POST'])
def setLogin():

    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()

    session['loggedinID'] = j.get('id', None)
    session['loggedinFirstName'] = j.get('first_name', None)
    session['loggedinLastName'] = j.get('last_name', None)
    session['loggedinUsername'] = j.get('username', None)
    session['loggedinSchoolId'] = j.get('school_id', None)
    session['loggedinEmail'] = j.get('email', None)
    session['loggedinCreatedOn'] = j.get('created_on', None)
    session['message'] = j.get('message', None)

    return jsonify([
        {
            'loggedinID': session['loggedinID'],
            'loggedinUsername': session['loggedinUsername'],
            'message' : session['message'],
        }
    ])


@app.route('/getLogin', methods=['GET'])
def getLogin():
    if session['loggedinID'] != None:
        return jsonify(
            {
                'loggedinID': session['loggedinID'],
                'loggedinFirstName': session['loggedinFirstName'],
                'loggedinLastName': session['loggedinLastName'],
                'loggedinUsername': session['loggedinUsername'],
                'loggedinSchoolId': session['loggedinSchoolId'],
                'loggedinEmail': session['loggedinEmail'],
                'loggedinCreatedOn': session['loggedinCreatedOn'],
            }
        )
    else:
        return jsonify( {'message': 'Not logged in'} )

db_create(db_options)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

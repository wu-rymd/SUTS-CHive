from flask import Flask, request, jsonify, render_template, Response
from lib.db import dbconnect, db_create, School, User, Club, UserToClubMapping
import json

app = Flask(__name__)

db_options = {'db_file': 'my.db'}


# TODO change CORS/Access-Control-Allow-Origin so not everyone can access db

def get_or_create_school(session, school_name, address):
    # TODO ensure not case sensitive
    # so new school won't be created for carelessness
    school_name = school_name
    school = session.query(School).filter(School.name == school_name).one_or_none()
    if school:
        return school.id
    school = School(name=school_name, address=address)
    session.add(school)
    session.flush()
    return school.id


@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    Session, engine = dbconnect(db_options)
    session = Session()
    users = session.query(User).filter(User.username == username).all()
    ret_users = []
    for u in users:
        ret_users.append(
            {
                'id': u.id,
                'username': u.username,
                'first': u.first_name,
                'last': u.last_name
            }
        )
    #users = map(lambda u: dict(u), users)
    response = jsonify(ret_users)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response





@app.route('/user', methods=['POST'])
def create_user():
    firstName = request.args.get('first_name')
    lastName = request.args.get('last_name')
    userName = request.args.get('username')
    eMail = request.args.get('email')
    schoolName = request.args.get('schoolName')
    schoolAddress = request.args.get('schoolAddress')

    Session, engine = dbconnect(db_options)
    session = Session()
    user = User(
        first_name=firstName,
        last_name=lastName,
        username=userName,
        email=eMail,
        school_id=get_or_create_school(session, schoolName, schoolAddress),
    )
    session.add(user)
    session.flush()
    session.commit()
    response = jsonify(
        {
            'id': user.id
        }
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



@app.route('/user', methods=['PUT'])
def modify_user():
    return 'UNIMPLEMENTED'


@app.route('/user', methods=['DELETE'])
def delete_user():
    return 'UNIMPLEMENTED'


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
    )
    session.add(club)
    session.flush()
    session.commit()
    response = jsonify(
        {
            'id': club.id
        }
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/club', methods=['PUT'])
def modify_club():
    return 'UNIMPLEMENTED'


@app.route('/club', methods=['DELETE'])
def delete_club():
    return 'UNIMPLEMENTED'


@app.route('/schools', methods=['POST'])
def create_school():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    school = get_or_create_school(session, j['name'], j['address'])
    session.commit()
    response = jsonify(
        {
            'id': school.id
        }
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    

@app.route('/schools', methods=['GET'])
def get_schools():
    Session, engine = dbconnect(db_options)
    session = Session()
    schools = session.query(School).all()
    print schools
    formatted_schools = []
    for s in schools:
        formatted_schools.append({
            'id': s.id,
            'name': s.name,
            'address': s.address
        })
    response = Response(json.dumps(formatted_schools))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db_create(db_options)
    app.run(host='0.0.0.0', debug=True)

from flask import Flask, request, jsonify, render_template, Response
from lib.db import dbconnect, db_create, School, User, Club, UserToClubMapping
import json

app = Flask(__name__)

db_options = {'db_file': 'my.db'}


def get_or_create_school(session, school_name, address):
    school = session.query(School).filter(School.name == school_name).one_or_none()
    if school:
        return school
    school = School(name=school_name, address=address)
    session.add(school)
    session.flush()
    return school.id


@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    Sesson, engine = dbconnect(db_options)
    session = Sesson()
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
    return jsonify(ret_users)


@app.route('/user', methods=['POST'])
def create_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Sesson, engine = dbconnect(db_options)
    session = Sesson()
    user = User(
        first_name=j.get('first_name'),
        last_name=j.get('last_name'),
        username=j.get('username'),
        school_id=get_or_create_school(session, j.get('school')),
        email=j.get('email')
    )
    session.add(user)
    session.flush()
    session.commit()
    return jsonify(
        {
            'id': user.id
        }
    )


@app.route('/user', methods=['PUT'])
def modify_user():
    return 'UNIMPLEMENTED'


@app.route('/user', methods=['DELETE'])
def delete_user():
    return 'UNIMPLEMENTED'


@app.route('/club', methods=['GET'])
def get_club():
    name = request.args.get('name')
    Sesson, engine = dbconnect(db_options)
    session = Sesson()
    clubs = session.query(Club).filter(Club.name == name).all()
    ret_clubs = []
    for c in clubs:
        ret_clubs.append(
            {
                'id': c.id,
                'username': c.name,
                'school': c.school_id,
            }
        )
    return jsonify(ret_clubs)


@app.route('/club', methods=['POST'])
def create_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Sesson, engine = dbconnect(db_options)
    session = Sesson()
    club = Club(
        name=j.get('name'),
        school_id=get_or_create_school(session, j.get('school'))
    )
    session.add(club)
    session.flush()
    session.commit()
    return jsonify(
        {
            'id': club.id
        }
    )


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
    school_id = get_or_create_school(session, j['name'], j['address'])
    session.commit()
    return jsonify(
        {
            'id': school_id
        }
    )

@app.route('/schools', methods=['GET'])
def get_schools():
    Session, engine = dbconnect(db_options)
    session = Session()
    schools = session.query(School).all()
    print schools
    formatted_schools = []
    for s in schools:
        formatted_schools.append({
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

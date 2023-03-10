import json
from flask import request
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from initialise import Initialise
from flask import Flask

#Creates the flask app
app = Flask(__name__)
init = Initialise()
app = init.db(app)

#Creates DB connection
db = SQLAlchemy(app)

def hateoas(id):
    return [
        {
            "rel": "self",
            "resource": "http://127.0.0.1:8000/v1/users" + str(id),
            "method": "GET"
        },
        {
            "rel": "update",
            "resource": "http://127.0.0.1:8000/v1/users" + str(id),
            "method": "PATCH"
        },
        {
            "rel": "update",
            "resource": "http://127.0.0.1:8000/v1/users" + str(id),
            "method": "DELETE"
        }
    ]

@app.route('/v1/users', methods=['POST'])
def post_user_details():
    try:
        data = request.get_json()
        sql = text('INSERT INTO users (name, surname, identity_number) values (:name, :surname, :id_num)')
        result = db.session.execute(
            sql,
            name=data['name'],
            surname=data['surname'],
            id_num=data['identity_number']
        )
        return json.dumps({"id": result.lastrowid,"links": hateoas(result.lastrowid)})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND
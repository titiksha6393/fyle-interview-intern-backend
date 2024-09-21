from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from core import app, db
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError

from core.models.assignments import Assignment

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')



@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response

print([str(rule) for rule in app.url_map.iter_rules()])

@app.route('/some-endpoint', methods=['POST'])
def some_endpoint():
    data = request.json
    # Example: Simulate adding a record that could cause an IntegrityError
    new_record = Assignment(**data)
    db.session.add(new_record)
    db.session.commit()  # This should be where the IntegrityError could occur
    return jsonify(success=True), 201


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code
    else:
        raise err

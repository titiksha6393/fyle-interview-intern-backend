from flask import Blueprint 
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/principal/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Lists all submitted and graded assignments"""
    all_assignments = Assignment.get_assignments_by_state()
    all_assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=all_assignments_dump)


@principal_assignments_resources.route('/principal/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """Lists all the teachers"""
    teachers = Teacher.get_all_teachers()
    # should the data be dumped in "AssignmentSchema or should I make another schema"
    teachers_dump = AssignmentSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_or_regrade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

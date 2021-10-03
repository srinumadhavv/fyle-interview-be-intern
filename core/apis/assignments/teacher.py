from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def submit_grade(p, incoming_payload):
    """Submit a grade"""
    submit_grade_payload = AssignmentGradeSchema().load(incoming_payload)
    teachr_id=p.teacher_id
    submitted_grade = Assignment.submit_grade(
        _id=submit_grade_payload.id,
        grade=submit_grade_payload.grade,
        principal=p,teachr_id=teachr_id
    )
    db.session.commit()
    submitted_grade_dump = AssignmentSchema().dump(submitted_grade)
    return APIResponse.respond(data=submitted_grade_dump)

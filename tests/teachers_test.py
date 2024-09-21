import pytest
from core.apis.assignments.schema import AssignmentSchema
from core.models.assignments import Assignment, AssignmentStateEnum
from core import db
from core.models.teachers import Teacher

def test_grade_assignment(client, h_teacher_2):
    # Step 1: Create a draft assignment
    submitted_assignment = Assignment(
        student_id=1,
        teacher_id=2,
        content="Draft assignment",
        grade=None,  # Initially, no grade is set
        state=AssignmentStateEnum.SUBMITTED
    )
    
    db.session.add(submitted_assignment)
    db.session.commit()

    print(f"Submitted Assignment ID: {submitted_assignment.id}")

    # Step 2: Prepare the payload for grading
    payload = {
        'id': submitted_assignment.id,
        'grade': 'A'  # Assign a grade
    }
    print(f"Payload: {payload}")

    # Step 3: Simulate the grading process
    response = client.post(
        '/teacher/assignments/grade',
        json=payload,
        headers=h_teacher_2
    )

    # Step 4: Check the response
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Data: {response.json}")

    assert response.status_code == 200
    graded_assignment = Assignment.query.get(submitted_assignment.id)
    print(f"Assignment State: {graded_assignment.state}")
    
    # Verify that the grade has been updated in the database
    assert graded_assignment.grade == 'A'

    # Verify the response data
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    assert response.json == {
        'data': graded_assignment_dump
    }

    # Optional: Clean up test data
    # db.session.delete(submitted_assign_assignment)
    # db.session.commit()

def test_grade_assignment_not_submitted(client, h_teacher_1):
    """
    Failure case: If an assignment state is not SUBMITTED, return 400 with FyleError.
    """
    # Step 1: Create a draft assignment
    draft_assignment = Assignment(
        student_id=1,
        teacher_id=1,
        content="Draft assignment",
        grade=None,
        state=AssignmentStateEnum.DRAFT  # Ensure it's in DRAFT state
    )
    
    db.session.add(draft_assignment)
    db.session.commit()

    print(f"Draft Assignment ID: {draft_assignment.id}")

    # Step 2: Prepare the payload for grading
    payload = {
        "id": draft_assignment.id,  # Use the ID of the draft assignment
        "grade": "A"  # Attempting to grade it
    }
    
    # Step 3: Simulate the grading process
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json=payload
    )

    # Step 4: Check the response
    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'  # Check for the FyleError


def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    submitted_assignment = Assignment(
        student_id=1,
        teacher_id=2,
        content="Draft assignment",
        grade="A",
        state=AssignmentStateEnum.DRAFT
    )
    
    db.session.add(submitted_assignment)
    db.session.commit()

    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200
    assert 'DRAFT' in [assignment['state'] for assignment in response.json['data']]

def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_submitted_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

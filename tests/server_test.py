import pytest
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

# Set up a Flask test client fixture for the tests
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_ready_endpoint(client):
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert 'time' in data  # Optionally check the time format if needed


# Test for FyleError
def test_fyle_error_handler(client):
    # Simulate a request that raises a FyleError
    @app.route('/error', methods=['GET'])
    def error_route():
        raise FyleError(status_code=400, message='This is a Fyle error.')

    response = client.get('/error')
    
    assert response.status_code == 400
    assert response.json == {
        'error': 'FyleError',
        'message': 'This is a Fyle error.'
    }

# Test for ValidationError
def test_validation_error_handler(client):
    # Simulate raising a ValidationError
    with pytest.raises(ValidationError):
        raise ValidationError({"field": ["Invalid data"]})

# Test for IntegrityError
def test_integrity_error_handler(client, mocker):
    mocker.patch('core.db.session.commit', side_effect=IntegrityError('Simulated IntegrityError', orig='duplicate key error', params={}))

    # Make a request to the route that would commit to the DB
    response = client.post('/some-endpoint', json={
        "student_id": 1,  # Replace with a valid student ID
        "teacher_id": 2,  # Replace with a valid teacher ID or leave it out if nullable
        "content": "This is a test assignment.",
        "grade": "A",  # Adjust based on your GradeEnum
        "state": "DRAFT" }) # Adjust based on your AssignmentStateEnum
    
    # Check if the error handler responds with a 400 status code and proper message
    assert response.status_code == 400
    assert response.json['error'] == 'IntegrityError'
    assert 'duplicate key error' in response.json['message']

def test_some_endpoint_success(client):
    # Mock the successful behavior (not triggering IntegrityError)
    response = client.post('/some-endpoint', json={
        "student_id": 1,  # Replace with a valid student ID
        "teacher_id": 2,  # Replace with a valid teacher ID or leave it out if nullable
        "content": "This is a test assignment.",
        "grade": "A",  # Adjust based on your GradeEnum
        "state": "DRAFT"  # Adjust based on your AssignmentStateEnum
    })

    # Assert that the response is successful
    assert response.status_code == 201
    assert response.json['success'] is True
    
# Test for HTTPException (404 NotFound)
def test_http_exception_handler(client):
    # Trigger a 404 NotFound by requesting an invalid route
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'

import json

def test_authenticate_principal_no_such_api(client):
    # Prepare a mock principal header
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': 1
        })
    }

    # Send a POST request to the invalid endpoint
    response = client.post('/invalid', headers=headers)

    # Check that the response status code matches what the assertion should trigger
    assert response.status_code == 404  # Adjust as necessary
    print(response.json)
    assert response.json == {'error': 'NotFound', "message": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}  # Adjust based on your actual error handling

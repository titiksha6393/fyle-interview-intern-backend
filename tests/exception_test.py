from core.libs.exceptions import FyleError


def test_fyle_error_to_dict():
    # Create an instance of your FyleError (or whatever class has the to_dict method)
    error = FyleError(message="This is a test error", status_code=400)
    
    # Call the to_dict method
    result = error.to_dict()
    
    # Check the contents of the result
    assert result == {'message': "This is a test error"}

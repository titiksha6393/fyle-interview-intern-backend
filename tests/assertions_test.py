import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

# Test assert_auth with False condition
def test_assert_auth():
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False)
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == 'UNAUTHORIZED'

# Test assert_true with False condition
def test_assert_true():
    with pytest.raises(FyleError) as excinfo:
        assert_true(False)
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == 'FORBIDDEN'

# Test assert_valid with False condition
def test_assert_valid():
    with pytest.raises(FyleError) as excinfo:
        assert_valid(False)
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == 'BAD_REQUEST'

# Test assert_found with None object
def test_assert_found():
    with pytest.raises(FyleError) as excinfo:
        assert_found(None)
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == 'NOT_FOUND'

from src.services.auth import AuthService

def test_encode_jwt_token():
    data = {"user_id": "1"}

    token = AuthService().encode_jwt_token(data)

    assert token
    assert isinstance(token, str)
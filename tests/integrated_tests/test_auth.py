from src.services.auth import AuthService


def test_encode_jwt_token():
    data = {"user_id": "1"}

    token = AuthService().encode_jwt_token(data)

    assert token
    assert isinstance(token, str)

    decoded_token = AuthService().decode_jwt_token(token)

    assert decoded_token
    assert decoded_token["user_id"] == data["user_id"]

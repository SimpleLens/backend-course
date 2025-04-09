import pytest


@pytest.mark.parametrize("email, password", [
    ("kaki_puki@mail.ru", "1234vfds5"),
    ("kaki_12puki@mail.ru", "12341vfds5")
])
async def test_auth_e2e(
        email,
        password,
        authenticated_ac
):
    response_register = await authenticated_ac.post(
        "/auth/register",
        json = {
            "email": email,
            "password": password
        }
    )

    assert response_register.status_code == 200

    response_login = await authenticated_ac.post(
        "/auth/login",
        json = {
            "email": email,
            "password": password
        }
    )

    assert response_login.status_code == 200
    assert response_login.cookies["access_token"]

    response_me = await authenticated_ac.get(
        "auth/me"
    )

    assert response_me.status_code == 200
    assert (response_me.json())["id"]

    response_logout = await authenticated_ac.post(
        "auth/logout"
    )

    assert response_logout.status_code == 200
    assert not response_logout.cookies.get("access_token")

    response_me = await authenticated_ac.get(
        "auth/me"
    )

    assert response_me.status_code == 401

    response_login = await authenticated_ac.post(
        "/auth/login",
        json = {
            "email": email,
            "password": password
        }
    )

    assert response_login.status_code == 200
    assert response_login.cookies["access_token"]

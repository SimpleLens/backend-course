import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kaki_puki@mail.ru", "1234vfds5", 200),
        ("kaki_12puki@mail.ru", "12341vfds5", 200),
        ("kaki_12puki@mail.ru", "12341vfds5", 400),
        ("kaki_12puki@mail", "12341vfds5", 422),
    ],
)
async def test_auth_e2e(email, password, status_code, ac):
    response_register = await ac.post("/auth/register", json={"email": email, "password": password})

    assert response_register.status_code == status_code
    if response_register.status_code != 200:
        return

    response_login = await ac.post("/auth/login", json={"email": email, "password": password})

    assert response_login.status_code == 200
    assert response_login.cookies["access_token"]

    response_me = await ac.get("auth/me")

    assert response_me.status_code == 200
    assert (response_me.json())["id"]

    response_logout = await ac.post("auth/logout")

    assert response_logout.status_code == 200
    assert not response_logout.cookies.get("access_token")

    response_me = await ac.get("auth/me")

    assert response_me.status_code == 401

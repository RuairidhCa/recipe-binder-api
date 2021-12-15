import pytest

from fixtures.client import client


def login(client, username, password):
    res = client.post("/api/login", json=dict(username=username, password=password))
    return res


def register(client, username, password):
    res = client.post("/api/register", json=dict(username=username, password=password))
    return res


def test_register(client):
    username = "test_user"
    password = "test_user_password"
    res = register(client, username, password)

    assert res.status_code == 201
    assert res.json["username"] == username
    assert res.json["id"] != None
    assert res.json["token"] != None


def test_register_duplicate_user(client):
    username = "test_user"
    password = "test_user_password"

    register(client, username, password)
    res = register(client, username, password)

    assert res.status_code == 409
    assert res.json["message"] == "A user with that username already exists."


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_login(client):
    username = "test_user"
    password = "test_user_password"

    register(client, username, password)
    res = login(client, username, password)

    assert res.status_code == 200
    assert res.json["username"] == username
    assert res.json["id"] != None
    assert res.json["token"] != None


def test_login_no_user(client):
    username = "test_user"
    password = "test_user_password"

    res = login(client, username, password)

    assert res.status_code == 400
    assert res.json["message"] == "Username or password incorrect"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_login_incorrect_password(client):
    username = "test_user"
    password = "test_user_password"

    register(client, username, password)
    res = login(client, username, "wrong_password")

    assert res.status_code == 400
    assert res.json["message"] == "Username or password incorrect"

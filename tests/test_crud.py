from fixtures.client import client


def get_token(client):
    register_res = client.post(
        "/api/register", json=dict(username="test_user", password="test_pass")
    )
    return register_res.json["token"]


def create_recipe(client, token=None):
    headers = dict(Authorization="Bearer " + token) if token != None else None
    res = client.post(
        "/api/recipes",
        headers=headers,
        json=dict(title="title", url="url", tags=["tag"]),
    )
    return res


def get_all_recipes(client):
    res = client.get("/api/recipes")
    return res


def update_recipe(client, token=None, recipe_id="1"):
    headers = dict(Authorization="Bearer " + token) if token != None else None
    res = client.put(
        "/api/recipes/" + recipe_id,
        headers=headers,
        json=dict(title="new_title", url="url", tags=["tag"]),
    )
    return res


def delete_recipe(client, token=None, recipe_id="1"):
    headers = dict(Authorization="Bearer " + token) if token != None else None
    res = client.delete(
        "/api/recipes/" + recipe_id,
        headers=headers,
    )
    return res


def test_create_recipe(client):
    token = get_token(client)
    res = create_recipe(client, token)
    assert res.status_code == 201


def test_get_all_recipes(client):
    res = get_all_recipes(client)
    assert res.status_code == 200
    assert res.json["data"] != None


def test_update_recipe(client):
    token = get_token(client)
    create_recipe(client, token)
    res = update_recipe(client, token)

    assert res.status_code == 204


def test_update_recipe_does_not_exist(client):
    token = get_token(client)
    res = update_recipe(client, token)

    assert res.status_code == 404


def test_delete_recipe(client):
    token = get_token(client)
    create_recipe(client, token)
    res = delete_recipe(client, token)

    assert res.status_code == 204


def test_delete_recipe_does_not_exist(client):
    token = get_token(client)
    res = delete_recipe(client, token)

    assert res.status_code == 404


def test_no_token(client):
    create_res = create_recipe(client)
    assert create_res.status_code == 401

    update_res = update_recipe(client)
    assert update_res.status_code == 401

    delete_res = delete_recipe(client)
    assert delete_res.status_code == 401

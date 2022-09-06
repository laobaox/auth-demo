import pytest
import requests
from auth_demo import config
from ..random_refs import random_name


def create_user(url_base, name=None):
    if not name:
        name = random_name()
    r = requests.post(
        f"{url_base}/users", json={"name": name, "password": "123"}
    )
    return name, r


def create_role(url_base, name=None):
    if not name:
        name = random_name()
    r = requests.post(
        f"{url_base}/roles", json={"name": name}
    )
    return name, r


def get_auth_token(url_base, name):
    r = requests.post(f"{url_base}/auth-tokens",
                         json={"name": name, "password": '123'})
    return r.json()['token']

def add_role_to_user(url_base, user_name, role_name):
    r = requests.post(f"{url_base}/users/{user_name}/roles", json={"name": role_name})
    assert r.status_code == 200

def test_create_user(url_base):
    name, r = create_user(url_base)
    assert r.status_code == 200

    name, r = create_user(url_base, name)
    assert r.status_code == 400


def test_delete_user(url_base):
    name = random_name()
    r = requests.delete(f"{url_base}/users/{name}")
    assert r.status_code == 404

    name, r = create_user(url_base, name)
    assert r.status_code == 200

    r = requests.delete(f"{url_base}/users/{name}")
    assert r.status_code == 200


def test_create_role(url_base):
    name, r = create_role(url_base)
    assert r.status_code == 200

    name, r = create_role(url_base, name)
    assert r.status_code == 400


def test_delete_role(url_base):
    name = random_name()
    r = requests.delete(f"{url_base}/roles/{name}")
    assert  r.status_code == 404

    name, r = create_role(url_base, name)
    assert r.status_code == 200

    r = requests.delete(f"{url_base}/roles/{name}")
    assert r.status_code == 200


def test_add_role_to_user(url_base):
    user_name = random_name()
    role_name = random_name()
    def send():
        return requests.post(f"{url_base}/users/{user_name}/roles", json={"name": role_name})
    r = send()
    assert r.status_code == 400
    create_user(url_base, user_name)
    r = send()
    assert r.status_code == 400
    create_role(url_base, role_name)
    r = send()
    assert r.status_code == 200


def test_auth(url_base):
    name = random_name()
    password = '123'
    def send(password=password):
        return requests.post(f"{url_base}/auth-tokens",
                             json={"name": name, "password": password})
    assert send().status_code == 400
    create_user(url_base, name)
    assert send('456').status_code == 400
    assert send().status_code == 200


def test_invalidate(url_base):
    name = random_name()
    token = 'not exists'
    def send(token):
        return requests.delete(f"{url_base}/auth-tokens/{token}")

    assert send(token).status_code == 404
    create_user(url_base, name)
    token = get_auth_token(url_base, name)
    assert send(token).status_code == 200

def test_check_role(url_base):
    name = random_name()
    role_name = random_name()

    def send(token):
        return requests.get(f"{url_base}/auth-tokens/{token}/role-checks/{role_name}")
    assert send("xxx").status_code == 400
    create_user(url_base, name)
    token = get_auth_token(url_base, name)
    assert send(token).status_code == 400
    create_role(url_base, role_name)
    add_role_to_user(url_base, name, role_name)
    r = send(token)
    assert r.status_code == 200
    assert r.json()['result'] == True

def test_get_token_roles(url_base):
    name = random_name()
    role_names = [random_name() for _ in range(3)]

    def send(token):
        return requests.get(f"{url_base}/auth-tokens/{token}/roles")

    assert send('notexists').status_code == 400
    create_user(url_base, name)
    token = get_auth_token(url_base, name)
    for role_name in role_names:
        create_role(url_base, role_name)
        add_role_to_user(url_base, name, role_name)
    r = send(token)
    assert r.status_code == 200
    assert set(r.json()['items']) == set(role_names)
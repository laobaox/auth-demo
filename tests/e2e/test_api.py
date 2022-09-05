
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


def add_role_to_user(url_base):
    pass





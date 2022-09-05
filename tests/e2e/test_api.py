
import requests
from auth_demo import config
from ..random_refs import random_name


def test_create_user():
    url = config.get_api_url()
    name = random_name()
    r = requests.post(
        f"{url}/users", json={"name": name, "password": "123"}
    )
    assert r.status_code == 200

    r = requests.post(
        f"{url}/users", json={"name": name, "password": "123"}
    )
    assert r.status_code == 400

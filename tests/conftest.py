import pytest
from auth_demo import config
from auth_demo.adapters import repository


@pytest.fixture(scope="session")
def url_base():
    return config.get_api_url()


@pytest.fixture
def user_repo():
    return repository.MemUserRepository(users={})


@pytest.fixture
def role_repo():
    return repository.MemRoleRepository(roles={})
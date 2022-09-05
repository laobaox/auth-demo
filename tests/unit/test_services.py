import pytest
from auth_demo.adapters import repository
from auth_demo.service_layer import services

def test_add_user_success_and_fail():
    user_repo = repository.MemUserRepository(users={})
    name = 'bob'
    password = '123'
    services.create_user(name, password, user_repo)
    users = user_repo.users
    assert len(users) == 1
    assert  users.values()[0].name == name
    with pytest.raises(services.UserExists):
        services.create_user(name, password, user_repo)


def test_delete_user_suc_and_fail():
    user_repo = repository.MemUserRepository(users={})
    name = 'bob'
    password = '123'
    services.create_user(name, password, user_repo)
    with pytest.raises(services.UserNotExists):
        services.delete_user('xyz', user_repo)
    services.delete_user(name)
    assert len(user_repo.users) == 0


def test_add_role_suc_and_fail():
    role_repo = user_repo = repository.MemRoleRepository(roles={})
    name = 'admin'
    services.create_role(name, role_repo)
    roles = role_repo.roles
    assert len(roles) == 1
    assert roles.values()[0].name == 'admin'

    with pytest.raises(services.RoleExists):
        services.create_role(name, role_repo)
    assert len(roles) == 1
    assert roles.values()[0].name == 'admin'

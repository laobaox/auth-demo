import pytest
from datetime import datetime
from auth_demo.service_layer import services
from auth_demo import setting
from auth_demo.lib import mem_token


def test_create_user(user_repo):
    name = 'bob'
    password = '123'
    services.create_user(name, password, user_repo)
    users = user_repo.users
    assert len(users) == 1
    assert next(iter(users.values())).name == name
    with pytest.raises(services.UserExists):
        services.create_user(name, password, user_repo)


def test_delete_user(user_repo):
    name = 'bob'
    password = '123'
    services.create_user(name, password, user_repo)
    with pytest.raises(services.UserNotExists):
        services.delete_user('xyz', user_repo)
    services.delete_user(name, user_repo)
    assert len(user_repo.users) == 0


def test_create_role(role_repo):
    name = 'admin'
    services.create_role(name, role_repo)
    roles = role_repo.roles
    assert len(roles) == 1
    assert next(iter(roles.values())).name == 'admin'

    with pytest.raises(services.RoleExists):
        services.create_role(name, role_repo)
    assert len(roles) == 1
    assert next(iter(roles.values())).name == 'admin'


def test_delete_role(role_repo):
    name = 'admin'
    with pytest.raises(services.RoleNotExists):
        services.delete_role(name, role_repo)
    services.create_role(name, role_repo)
    assert len(role_repo.roles) == 1
    services.delete_role(name, role_repo)
    assert len(role_repo.roles) == 0


def test_add_role_to_user(user_repo, role_repo):
    user_name = 'bob'
    password = '123'
    role_name = 'admin'
    services.create_user(user_name,  password, user_repo)
    services.create_role(role_name, role_repo)
    services.add_role_to_user(user_name, role_name, user_repo, role_repo)
    user = user_repo.get_by_name(user_name)
    role = role_repo.get_by_name(role_name)
    assert len(user.roles) == 1
    user_role = next(iter(user.roles))
    assert (role.id, role.name) == (user_role.id, user_role.name)


def test_auth_user(user_repo):
    name = 'bob'
    password = '123'
    with pytest.raises(services.UserNotExists):
        services.auth_user(name, password, user_repo)

    services.create_user(name, password, user_repo)
    token = services.auth_user(name, password, user_repo)
    assert token.data.name == 'bob'
    assert len(token.key) == setting.AUTH_TOKEN_SIZE
    expire_seconds = setting.AUTH_TOKEN_EXPIRE_HOURS * 3600
    assert expire_seconds-2<(token.expire_time - datetime.now()).total_seconds()<=expire_seconds


def prepare_token(user_repo):
    name = 'bob'
    password = '123'
    services.create_user(name, password, user_repo)
    return services.auth_user(name, password, user_repo)


def test_invalidate_token(user_repo):
    token = 'not exists'
    with pytest.raises(services.TokenIvalid):
        services.invalidate_token(token)

    token = prepare_token(user_repo)
    services.invalidate_token(token.key)
    assert mem_token.TokenStore.get(token.key) is None


def test_check_role(user_repo, role_repo):
    token_key = 'not exist'
    role_name = 'admin'
    with pytest.raises(services.TokenIvalid):
        services.check_role(token_key, role_name, role_repo)

    token = prepare_token(user_repo)
    services.create_role(role_name, role_repo)
    assert not services.check_role(token.key, role_name, role_repo)

    services.add_role_to_user(token.data.name, role_name, user_repo, role_repo)
    assert services.check_role(token.key, role_name, role_repo)


def get_token_roles(user_repo, role_repo):
    token_key = 'not exist'
    role_name = 'admin'
    with pytest.raises(services.TokenIvalid):
        services.get_token_roles(token_key)
    token = prepare_token(user_repo)
    assert tuple(services.get_token_roles(token.key)) == ()
    services.add_role_to_user(token.data.name, role_name, user_repo, role_repo)
    assert tuple(services.get_token_roles(token.key)) == (role_name,)
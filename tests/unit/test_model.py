from datetime import datetime
from auth_demo.domain import model
from auth_demo.lib import helpers

def new_user():
    salt = 'salt'
    id = 'user1'
    name = 'username1'
    password = '123'
    password_hash = helpers.calc_password_hash(password, salt)
    return model.User(id, name, salt, password_hash, datetime.now())


def new_role():
    id = 'role1'
    name = 'rolename1'
    return model.Role(id, name, datetime.now())


def test_user():
    user = new_user()
    role = new_role()
    assert not user.has_role(role)

    user.add_role(role)
    assert len(user.roles) == 1
    assert next(iter(user.roles)) == role
    assert len(role.users) == 1
    assert next(iter(role.users)) == user
    assert user.has_role(role)
    assert tuple(user.list_roles()) == (role,)


def test_role():
    user = new_user()
    role = new_role()
    assert role.is_users_empty()
    role.add_user(user)
    assert tuple(role.users) == (user,)
    assert not role.is_users_empty()
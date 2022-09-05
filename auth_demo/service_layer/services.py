import hashlib
import uuid
from datetime import datetime

from ..lib import helpers, user_token
from .. import setting
from ..domain import model


class UserExists(Exception):
    pass


class UserNotExists(Exception):
    pass


class RoleExists(Exception):
    pass


class RoleNotExists(Exception):
    pass


class PasswordError(Exception):
    pass


class TokenIvalid(Exception):
    pass


def create_user(name, password, user_repo):
    if user_repo.get_by_name(name):
        raise UserExists('user name exists')
    salt = helpers.random_str(setting.SALT_SIZE)
    id = helpers.gen_uniq_id()
    password_hash = helpers.calc_password_hash(password, salt)
    user = model.User(id, name, salt, password_hash, datetime.now())
    user_repo.add(user)


def delete_user(name, user_repo):
    user = user_repo.get_by_name(name)
    if not user:
        raise UserNotExists('user not exists')
    user_repo.delete(user)


def create_role(name, role_repo):
    if role_repo.get_by_name(name):
        raise RoleExists('role exsits')
    role = model.Role(helpers.gen_uniq_id(), name, datetime.now())
    role_repo.add(role)


def add_role_to_user(user_name, role_name, user_repo, role_repo):
    user = user_repo.get_by_name(user_name)
    if not user:
        raise UserNotExists('user not exists')
    role = role_repo.get_by_name(role_name)
    if not role:
        raise RoleNotExists('role not exist')
    user.add_role(role)


def auth_user(name, password, user_repo):
    user = user_repo.get_by_name(name)
    if not user:
        raise UserNotExists('user not exists')
    if not user.check_password(password):
        raise PasswordError('password is error')
    return user_token.TokenStore.create(user)


def invalidate_token(key):
    if not user_token.TokenStore.exists(key):
        raise TokenIvalid('token invalid')
    user_token.TokenStore.delete(key)


def check_role(key, role_name, role_repo):
    token = user_token.TokenStore.get(key)
    if not token:
        raise TokenIvalid('token invalid')
    user = token.data
    role = role_repo.get_by_name(role_name)
    return user.has_role(role)


def get_token_roles(key):
    token = user_token.TokenStore.get(key)
    if not token:
        raise TokenIvalid('token invalid')
    roles = token.data.list_roles()
    return [role.name for role in roles]
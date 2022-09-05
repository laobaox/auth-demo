#-*- coding: utf8 -*-

import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_name(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity):
        raise NotImplementedError

MEM_USERS = {}
MEM_ROLES = {}
class MemUserRepository(AbstractRepository):
    def __init__(self, users=MEM_USERS):
        self.users = users

    def add(self, user):
        self.users[user.name] = user

    def get_by_name(self, name):
        return self.users.get(name)

    def delete(self, user):
        self.users.pop(user.name, None)


class MemRoleRepository(AbstractRepository):
    def __init__(self, roles=MEM_ROLES):
        self.roles = roles

    def add(self, role):
        self.roles[role.name] = role

    def get_by_name(self, name):
        return self.roles.get(name, None)

    def delete(self, role):
        self.roles.pop(role.name, None)


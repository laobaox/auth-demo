from ..lib import helpers

# attention the method: __eq__ and __hash__
# __eq__ and __hash__ is override to save set colletion with name as hash key

class User(object):
    def __init__(self, id, name, salt, password_hash, ctime):
        self.id = id
        self.name = name
        self.salt = salt
        self.password_hash = password_hash
        self.ctime = ctime
        self.roles = set()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self, ):
        return hash(self.name)

    def check_password(self, password):
        return helpers.calc_password_hash(password, self.salt) == self.password_hash

    def add_role(self, role):
        # with __eq__ and __hash__ override,
        # role and user will store in the set collection with name as hash key
        # add user to role for limit deleting in use role
        self.roles.add(role)
        role.add_user(self)

    def has_role(self, role):
        return role in self.roles

    def list_roles(self):
        return list(self.roles)


class Role(object):
    def __init__(self, id, name, ctime):
        self.id = id
        self.name = name
        self.ctime = ctime
        self.users = set()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self, ):
        return hash(self.name)

    def add_user(self, user):
        self.users.add(user)

    def is_users_empty(self):
        return len(self.users) == 0
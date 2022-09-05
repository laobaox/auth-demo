
from auth_demo.adapters import repository
from auth_demo.service_layer import services

def test_user_repository():
    repo = repository.MemUserRepository()
    user_items = (
        ('bob1', '123,'),
        ('bob2', '456,'),
        ('bob3', '789,'),
    )
    for name, password in user_items:
        services.create_user(name, password, repo)
    created_user_items = [user.name for user in repository.MEM_USERS.values()]
    assert tuple([item[0] for item in user_items]) == tuple(created_user_items)


def test_role_repository():
    repo = repository.MemRoleRepository()
    names = [
        'admin1',
        'admin2',
        'admin3',
    ]
    for name in names:
        services.create_role(name, repo)
    assert tuple([role.name for role in repository.MEM_ROLES.values()]) == tuple(names)
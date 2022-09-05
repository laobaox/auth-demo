import uuid


def random_name():
    return uuid.uuid4().hex[:10]

#-*- utf8 -*-

import hashlib
import uuid
import string
import random


def random_str(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(size))

def gen_uniq_id():
    return str(uuid.uuid4())

def calc_password_hash(password, salt):
    s = password + salt
    return hashlib.sha256(s.encode('utf8')).hexdigest()
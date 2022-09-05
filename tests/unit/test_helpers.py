
from auth_demo.lib import helpers
from auth_demo import setting

def test_random_str():
    size = 32
    s1 = helpers.random_str(size)
    s2 = helpers.random_str(size)
    assert isinstance(s1, str) and isinstance(s2, str)
    assert len(s1) == size and len(s2) == size
    assert s1 != s2

def test_gen_uniq_id():
    size = 36
    s1 = helpers.gen_uniq_id()
    s2 = helpers.gen_uniq_id()
    assert len(s1) == size and len(s2) == size
    assert s1 != s2

def test_calc_password_hash():
    password = '123'
    salt = 'xyzabc'
    ans = '252c886587d59116596bc2926854eca1bc75c4cf0ab61490c066edc8f34b59b4'
    assert helpers.calc_password_hash(password, salt) == ans

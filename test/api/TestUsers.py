import unittest
from source.api.Users import *
from source.framework.ApiServiceHandler import dummy_user


# mock a user
user = dummy_user()

# learn how to mock!


class TestApiMethods(unittest.TestCase):

    def test_get_user_success(self):
        response = get_user(user, user.get_id())
        assert response['status'] == "200"

    def test_get_user_fail_wronguser(self):
        response = get_user(user, user.get_id()+1)
        assert response['status'] == "403"

    def test_create_user_success(self):
        response = create_user("a@b.com", "a", "b", "sms")
        assert response['status'] == "200"

    # try to test using the same email
    def test_create_user_fail(self):
        response = create_user("a@b.com", "a", "b", "sms")
        assert response['status'] == "403"



if __name__ == '__main__':
    unittest.main()

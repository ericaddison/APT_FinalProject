import unittest
from source.api.Conversations import get_conversations


class TestApiMethods(unittest.TestCase):

    def test_get_conversations_all(self):
        convs = get_conversations()
        assert convs == "All conversations"

    def test_create_conversation(self):
        assert False

    def test_create_conversation(self):
        assert False


if __name__ == '__main__':
    unittest.main()

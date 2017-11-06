import unittest
from source.api.get_conversations import get_conversations


class TestApiMethods(unittest.TestCase):

    def test_get_conversations_all(self):
        convs = get_conversations()
        assert convs == "All Conversations"


if __name__ == '__main__':
    unittest.main()

import unittest
import source.framework.webapp2_helpers as fh


class TestWebApp2Methods(unittest.TestCase):

    def test_make_routes(self):
        route = '/route1'
        app = fh.make_routes([(route, self.__class__)])
        assert app is not None
        assert route == app.router.match_routes[0].template
        assert self.__class__ == app.router.match_routes[0].handler


if __name__ == '__main__':
    unittest.main()

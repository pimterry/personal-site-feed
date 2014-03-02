import unittest
from unittest.mock import Mock, patch

from personal_feed.routes import setup_routes

class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = AppMock()
        setup_routes(self.app)

    def test_root_route_throws_no_exceptions(self):
        self.app['/']()

class AppMock:
    """
    Acts as a mock flask app, but only recording the routes,
    so they can be then easily accessed for testing later.
    """

    def __init__(self):
        self.routes = {}

    def route(self, route, *args, **kwargs):
        return self.decoratorFor(route)

    def decoratorFor(self, route):
        def decorator(routeTarget):
            self.routes[route] = routeTarget
            return routeTarget
        return decorator

    def __getitem__(self, item):
        return self.routes[item]
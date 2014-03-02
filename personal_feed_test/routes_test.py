import unittest
from unittest.mock import Mock, patch

from personal_feed.routes import setup_routes

@patch("personal_feed.routes.render_template")
class RoutesTests(unittest.TestCase):
    def setUp(self):
        feed_source = Mock(**{"feed_items": []})
        self.app = AppMock()
        setup_routes(self.app, feed_source)

    def test_root_route_throws_no_exceptions(self, renderer):
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
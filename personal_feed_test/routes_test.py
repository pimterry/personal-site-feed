import unittest, re
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

    def test_blog_route_redirect_is_permanent(self, renderer):
        result = self.app['/blog/*/*']("post")
        self.assertEqual(301, result.status_code)

    def test_blog_route_swaps_underscores_for_dashes(self, renderer):
        result = self.app['/blog/*/*']("post_post_post")
        self.assertEqual("http://blog.tim-perry.co.uk/post-post-post",
                         result.location)

    def test_blog_route_forces_lowercasing(self, renderer):
        result = self.app['/blog/*/*']("Post")
        self.assertEqual("http://blog.tim-perry.co.uk/post",
                         result.location)

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
        route = re.sub("<.*?>", "*", route)
        def decorator(routeTarget):
            self.routes[route] = routeTarget
            return routeTarget
        return decorator

    def __getitem__(self, item):
        return self.routes[item]

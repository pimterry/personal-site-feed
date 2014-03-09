import os
import cherrypy
from flask import Flask

from personal_feed.routes import setup_routes

from personal_feed.github.github_feed import GithubFeed
from personal_feed.twitter.twitter_feed import TwitterFeed
from personal_feed.aggregated_feed import AggregatedFeed


def build_app():
    app = Flask("Personal Feed")

    twitter_feed = TwitterFeed(os.environ["TWITTER_APP_KEY"],
                               os.environ["TWITTER_APP_TOKEN"],
                               os.environ["TWITTER_ACCESS_TOKEN"],
                               os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
                               os.environ["TWITTER_USERNAME"])

    setup_routes(app, AggregatedFeed([GithubFeed("pimterry"),
                                      twitter_feed]))
    return app

def run_server(app):
    cherrypy.tree.graft(app, '/')

    cherrypy.config.update({
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': int(os.environ.get('PORT', '8080')),
        'server.socket_host': '0.0.0.0'
    })

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    app = build_app()
    app.debug = True
    run_server(app)
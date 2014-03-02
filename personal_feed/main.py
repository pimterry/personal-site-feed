import os
import cherrypy
from flask import Flask, json

from personal_feed.routes import setup_routes
from personal_feed.github_feed import GithubFeed

def build_app():
    app = Flask("Personal Feed")
    setup_routes(app, GithubFeed())
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
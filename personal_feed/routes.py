def setup_routes(app):
    @app.route("/")
    def rootPage():
        return ""
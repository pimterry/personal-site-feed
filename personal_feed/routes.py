from flask import render_template

def setup_routes(app, feed_source):
    @app.route("/")
    def home_page():
        rendered_items = (render_template("items/%s" % item.feed_template, item=item)
                          for item in feed_source.feed_items)

        return render_template("feed.html", feed_items = list(rendered_items))
from flask import render_template, redirect

def setup_routes(app, feed_source):
    @app.route("/")
    def home_page():
        rendered_items = (render_template("items/%s" % item.feed_template, item=item)
                          for item in feed_source.feed_items)

        return render_template("feed.html", feed_items = list(rendered_items))

    @app.route("/blog/<path:date>/<post_name>")
    def blog_redirect(post_name, date=None):
        post_name = post_name.replace("_", "-").lower()
        return redirect("http://blog.tim-perry.co.uk/%s" % post_name, 301)

import atexit
import os

from flask import Flask

# register the database commands
from db import init_app

# apply the blueprints to the app
from blueprints import auth
from blueprints import index
from blueprints import record


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(
            app.instance_path, "flask-video-streaming.sqlite"),
        RECORDINGS_FOLDER=os.path.join(app.root_path, "recordings")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(index)
    app.register_blueprint(record)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', threaded=True)

print("IS THIS EVEN RUNNING?????",flush=True)

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.jinja_env.globals.update(int=int)
    app.jinja_env.globals.update(str=str)


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import nutweb
    app.register_blueprint(nutweb.bp)

    return app

if __name__ == '__main__':
    app=create_app()
    # host must be 0.0.0.0, otherwise won't work from inside docker container
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port=5001)

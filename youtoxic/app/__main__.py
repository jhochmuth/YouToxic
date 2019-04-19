import click

from flask import Flask

from flask_bootstrap import Bootstrap

from youtoxic.app import dash_view
from youtoxic.app import routes


@click.group()
def main():
    pass


@main.command()
@click.option("--debug", envvar="DEBUG", default=False, help="debug mode")
@click.option("--host", envvar="HOST", default="127.0.0.1", help="host IP address")
@click.option("--port", envvar="PORT", default=8050, help="port")
def runserver(debug, host, port):
    """Constructs the core application.

    Parameters
    ----------
    debug : bool
        Starts app in debug mode if True.
    host : str
        Flask will use this host value.
    port : int
        The port of the webserver.

    Returns
    -------
    None

    """
    app = Flask(__name__, instance_relative_config=False)
    bootstrap = Bootstrap(app)  # noqa
    dash_app = dash_view.add_dash(app)  # noqa

    app.register_blueprint(routes.main_bp)
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    main()

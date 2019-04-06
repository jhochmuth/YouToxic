import click

from flask import Flask

from flask_bootstrap import Bootstrap

from youtoxic.app import dash_view
from youtoxic.app import routes


@click.group()
def main():
    pass


@main.command()
def runserver():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    bootstrap = Bootstrap(app)
    dash_app = dash_view.add_dash(app)

    # Construct the core application
    app.register_blueprint(routes.main_bp)

    app.run()


if __name__ == "__main__":
    main()

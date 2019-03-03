import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from waitress import serve
#from config import Config


@click.group()
def main():
    pass


@main.command()
@click.option("--debug", envvar="DEBUG", default=False)
def runserver(debug):
    import toxicity_analysis.app.context as ctx
    app = ctx.create_app()
    app.config["DEBUG"] = debug

    from toxicity_analysis.app import routes

    bootstrap = Bootstrap(app)
    #app.config.from_object(Config)

    #db = SQLAlchemy(toxicity_analysis)
    #migrate = Migrate(toxicity_analysis, db)

    if debug:
        app.run(host="127.0.0.1", port=8080)

    else:
        serve(
            app,
            listen="127.0.0.1:8080",
            threads=5,
            send_bytes=18000
        )


if __name__ == '__main__':
    main()

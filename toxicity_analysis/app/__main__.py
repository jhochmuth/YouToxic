from logging import getLogger
from logging.config import dictConfig

import click

from waitress import serve

import yaml


def init_logging():
    with open("log-config.yml", "r") as f:
        log_config = yaml.safe_load(f)
        dictConfig(log_config)



@click.group()
def main():
    pass


@main.command()
@click.option(
    "--debug", envvar="DEBUG", default=False, help="Enable/disable debug mode"
)
@click.option(
    "--host", envvar="HOST", default="127.0.0.1", help="Host to run server on"
)
@click.option("--port", envvar="PORT", default=8080, help="Port to list on")
@click.option(
    "--threads",
    envvar="THREADS",
    default=5,
    help="The number of threads used to process application logic",
)
@click.option(
    "--send_bytes",
    envvar="SEND_BYTES",
    default=18000,
    help="The number of bytes to send to socket.send",
)
def runserver(debug, host, port, threads, send_bytes):
    import toxicity_analysis.app.context as ctx

    app = ctx.create_app()
    app.config["DEBUG"] = debug

    init_logging()
    logger = getLogger(__name__)

    from toxicity_analysis.app import routes # noqa

    # app.config.from_object(Config)

    # db = SQLAlchemy(toxicity_analysis)
    # migrate = Migrate(toxicity_analysis, db)

    if debug:
        logger.info(f"Starting {__name__} in debug mode")
        app.run(host=host, port=port)

    else:
        serve(
            app,
            listen=f"{host}:{port}",
            threads=threads,
            send_bytes=send_bytes
        )


if __name__ == "__main__":
    main()

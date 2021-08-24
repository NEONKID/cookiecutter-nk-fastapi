from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from shared.errors.handler import init_error_handler
from shared.middlewares import add_middlewares
from shared.routes import add_routes

from manager.src.containers import Container


def create_app():
    logger.info("Initializing {{cookiecutter.project_name}} manager..")

    container = Container()
    container.wire(modules=[])

    app = FastAPI(
        title="{{cookiecutter.project_name}} Manager API",
        default_response_class=ORJSONResponse,
        version="0.1",
        description="{{cookiecutter.project_short_description}}",
        docs_url=None,
        redoc_url=None,
        responses={415: {}},
    )
    app.container = container

    logger.info("Add middlewares..")
    app.add_middleware(CORSMiddleware,
                       allow_origins=container.config.cors().get('origin'),
                       allow_methods=container.config.cors().get('methods'),
                       allow_headers=container.config.cors().get('headers'))
    add_middlewares([], app)

    logger.info("Add Routes..")
    add_routes([], app)

    logger.info("Initialize error handler..")
    init_error_handler(app)

    @app.on_event("startup")
    async def on_startup():
        logger.info("Starting {{cookiecutter.project_name}} manager..")

        # TODO: startup code

        logger.info("Started {{cookiecutter.project_name}} manager..")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Stopping {{cookiecutter.project_name}} manager..")

        # TODO: shutdown code

        logger.info("Stopped {{cookiecutter.project_name}} manager..")

    return app

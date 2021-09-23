from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger
from pydantic import EmailStr

from common.errors.handler import init_error_handler
from common.middlewares import add_middlewares
from common.routes import add_routes

from service.src.containers import Container


def create_app(create_db: bool = False):
    logger.info("Initializing {{cookiecutter.project_name}} service..")

    container = Container()
    container.wire(modules=[])

    app = FastAPI(
        title="{{cookiecutter.project_name}} Service API",
        default_response_class=ORJSONResponse,
        version="0.1",
        description="{{cookiecutter.project_short_description}} 서비스 API",
        docs_url=None,
        redoc_url=None,
        responses={415: {}},
    )
    app.container = container
    db = container.db()

    logger.info("Add middlewares..")
    app.add_middleware(CORSMiddleware,
                       allow_origins=container.config.cors().get('origin'),
                       allow_methods=container.config.cors().get('methods'),
                       allow_headers=container.config.cors().get('headers'))
    add_middlewares([], app)

    logger.info("Add Routes..")
    add_routes([], app)

    logger.info("Initialize error handler..")
    init_error_handler(app, EmailStr("{{cookiecutter.project_author_email}}"))

    @app.on_event("startup")
    async def on_startup():
        logger.info("Starting {{cookiecutter.project_name}} service..")

        await db.connect()
        if create_db:
            await db.create_database()

        # TODO: startup code

        logger.info("Started {{cookiecutter.project_name}} service..")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Stopping {{cookiecutter.project_name}} service..")

        # TODO: shutdown code

        logger.info("Stopped {{cookiecutter.project_name}} service..")

    return app

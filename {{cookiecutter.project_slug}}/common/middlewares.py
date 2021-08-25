def add_middlewares(middlewares, app):
    from loguru import logger

    for middleware in middlewares:
        app.add_middleware(middleware)
        logger.debug("Add middleware: {}".format(middleware.__name__))

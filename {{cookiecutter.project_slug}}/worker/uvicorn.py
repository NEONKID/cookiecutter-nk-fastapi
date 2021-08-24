from uvicorn.workers import UvicornWorker


class AppWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "limit_concurrency": 50
    }

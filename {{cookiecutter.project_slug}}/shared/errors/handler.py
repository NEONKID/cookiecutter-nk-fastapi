from fastapi import status, Request, FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import ORJSONResponse, PlainTextResponse

from shared.errors import BadRequestException, ConflictException


def init_error_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def internal_server_error_handle(req: Request, exc: Exception):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'title': type(exc).__name__,
                'description': str(exc) + ', Contact me ({{cookiecutter.project_author_email}})'
            }
        )

    @app.exception_handler(RequestValidationError)
    async def request_exception_handle(req: Request, exc: RequestValidationError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'title': 'invalid:data',
                'description': '잘못된 요청 값',
                'extra': exc.errors()
            }
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_handle(req: Request, exc: BadRequestException):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'title': exc.title,
                'description': exc.detail
            }
        )

    @app.exception_handler(PyJWTError)
    async def unauthorized_handle(req: Request, exc: PyJWTError):
        return PlainTextResponse(status_code=status.HTTP_401_UNAUTHORIZED)

    @app.exception_handler(ConflictException)
    async def conflict_handle(req: Request, exc: ConflictException):
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'title': exc.title,
                'description': exc.detail
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(req: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_400_BAD_REQUEST:
            return await bad_request_handle(req, exc)
        elif exc.status_code == status.HTTP_409_CONFLICT:
            return await conflict_handle(req, exc)
        elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return await internal_server_error_handle(req, exc)
        return PlainTextResponse(status_code=exc.status_code)
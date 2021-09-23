from fastapi import status, Request, FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import ORJSONResponse, PlainTextResponse
from pydantic import EmailStr

from common.errors import BadRequestException, ConflictException
from common.utils.api import error, error_extended
from common.utils.api.template import schema


def init_error_handler(app: FastAPI, admin_email: EmailStr):
    @app.exception_handler(Exception)
    async def internal_server_error_handle(req: Request, exc: Exception):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_extended(
                exc, 'Occurred Internal Server Error, Contact me ({})'.format(admin_email),
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(exc))
        )

    @app.exception_handler(RequestValidationError)
    async def request_exception_handle(req: Request, exc: RequestValidationError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_extended(exc, schema[400]["content"]["application/json"]["example"]["error"]["message"],
                                   status.HTTP_400_BAD_REQUEST, exc.errors())
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_handle(req: Request, exc: BadRequestException):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error(exc.title, status.HTTP_400_BAD_REQUEST)
        )

    @app.exception_handler(StarletteHTTPException)
    async def bad_request_handle(req: Request, exc: StarletteHTTPException):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error(exc.detail, status.HTTP_400_BAD_REQUEST)
        )

    @app.exception_handler(PyJWTError)
    async def unauthorized_handle(req: Request, exc: PyJWTError):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_extended(exc, '인증 정보가 없거나 만료되었습니다', status.HTTP_401_UNAUTHORIZED, str(exc))
        )

    @app.exception_handler(StarletteHTTPException)
    async def unauthorized_handle(req: Request, exc: StarletteHTTPException):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handle(req: Request, exc: ForbiddenException):
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error(exc.title, status=status.HTTP_403_FORBIDDEN)
        )

    @app.exception_handler(StarletteHTTPException)
    async def forbidden_handle(req: Request, exc: StarletteHTTPException):
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error(exc.detail, status=status.HTTP_403_FORBIDDEN)
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handle(req: Request, exc: NotFoundException):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error(message=exc.title, status=status.HTTP_404_NOT_FOUND)
        )

    @app.exception_handler(StarletteHTTPException)
    async def not_found_handle(req: Request, exc: StarletteHTTPException):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error(message=exc.detail, status=status.HTTP_404_NOT_FOUND)
        )

    @app.exception_handler(ConflictException)
    async def conflict_handle(req: Request, exc: ConflictException):
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_extended(exc, exc.title, status.HTTP_409_CONFLICT, exc.detail)
        )

    @app.exception_handler(StarletteHTTPException)
    async def conflict_handle(req: Request, exc: StarletteHTTPException):
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error(message=exc.detail, status=status.HTTP_409_CONFLICT)
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(req: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_400_BAD_REQUEST:
            return await bad_request_handle(req, exc)
        elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return await unauthorized_handle(req, exc)
        elif exc.status_code == status.HTTP_403_FORBIDDEN:
            return await forbidden_handle(req, exc)
        elif exc.status_code == status.HTTP_404_NOT_FOUND:
            return await not_found_handle(req, exc)
        elif exc.status_code == status.HTTP_409_CONFLICT:
            return await conflict_handle(req, exc)

        return await internal_server_error_handle(req, exc)

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import Any, Generic, TypeVar, Optional

_T = TypeVar('_T')


class ApiError(BaseModel):
    exc: Optional[str] = Field(title="Exception 이름")
    message: str = Field(title="Exception 메시지")
    status: int = Field(title="HTTP 상태 코드")
    detail: Optional[Any] = Field(None, title="오류 상세")

    def __str__(self) -> str:
        return super().__str__()


class ApiResult(GenericModel, Generic[_T]):
    success: bool = Field(title="요청 성공 여부")
    response: Optional[_T] = Field(
        title="요청 성공 여부가 true 이면, response data가 존재하나, false 이면, 아무런 값도 제공해주지 않음")
    error: Optional[ApiError] = Field(title="요청 성공 여부가 false 이면, error 데이터를 제공", example=None)

    def __str__(self) -> str:
        return super().__str__()


def success(response: _T) -> dict:
    return {'success': True, 'response': response, 'error': None}


def error(message: str, status: int) -> dict:
    return {'success': False, 'response': None, 'error': {'message': message, 'status': status}}


def error_extended(exc: Exception, message: str, status: int, detail: Any) -> dict:
    return {
        'success': False, 'response': None,
        'error': {'exc': type(exc).__name__, 'message': message, 'status': status, 'detail': detail}
    }

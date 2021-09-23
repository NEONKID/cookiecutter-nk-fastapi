from typing import List

from common.utils.api import ApiResult

schema = {
    301: {},
    400: {
        "model": ApiResult,
        "description": "데이터의 타입이 맞지 않거나, 잘못 입력된 경우 (Bad Request)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None,
                    "error": {
                        "exc": "RequestValidationError", "message": "요청 값이 잘못 입력되었습니다", "status": 400,
                        "detail": [
                            {
                                "loc": [
                                    "body", "nickname"
                                ],
                                "msg": "string does not match regex \"^[a-zA-Z]*$\"",
                                "type": "value_error.str.regex",
                                "ctx": {
                                    "pattern": "^[a-zA-Z]*$"
                                }
                            },
                            {
                                "loc": [
                                    "body", "email"
                                ],
                                "msg": "value is not a valid email address",
                                "type": "value_error.email"
                            }
                        ]
                    }
                }
            }
        }
    },
    401: {
        "model": ApiResult,
        "description": "인증 토큰이 입력되지 않은 경우 (Unauthorized)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None, "error": {"status": 401, "message": "인증 정보가 없습니다"}
                }
            }
        }
    },
    403: {
        "model": ApiResult,
        "description": "해당 API에 권한이 없는 경우 (Forbidden)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None,
                    "error": {"status": 403, "message": "해당 요청에 대한 권한이 없습니다"}
                }
            }
        }
    },
    404: {
        "model": ApiResult,
        "description": "요청한 데이터가 존재하지 않는 경우 (Not Found)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None,
                    "error": {"status": 404, "message": "요청한 데이터를 찾을 수 없습니다"}
                }
            }
        }
    },
    409: {
        "model": ApiResult,
        "description": "요청한 데이터가 중복 혹은 다른 데이터와 충돌이 되는 경우 (Conflict)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None,
                    "error": {"status": 409, "message": "일부 데이터와 충돌이 있습니다"}
                }
            }
        }
    },
    415: {
        "model": ApiResult,
        "description": "서버가 지원하지 않는 content-type을 선택한 경우 (Unsupported Media Type)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None, "error": {"status": 415, "message": "지원하지 않는 요청 타입입니다"}
                }
            }
        }
    },
    422: {"description": "해당 오류는 400으로 대체 됨 (Unprocessable Entity)"},
    500: {
        "model": ApiResult,
        "description": "서버가 요청을 처리하는 중 내부 오류가 발생하는 경우 (Internal Server Error)",
        "content": {
            "application/json": {
                "example": {
                    "success": False, "response": None,
                    "error": {"exc": "Exception", "status": 500, "message": "Internal Server Error", "detail": {}}
                }
            }
        }
    }
}


def choose_template(req: List[int]) -> dict:
    res = {}
    for idx in req:
        res[idx] = schema[idx]

    return res

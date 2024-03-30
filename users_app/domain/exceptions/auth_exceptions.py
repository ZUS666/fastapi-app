from core.exceptions import AppException


class InvalidTokenError(AppException):
    status_code = 401
    detail = 'Invalid token'

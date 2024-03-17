from core.exceptions import AppException


class UserNotFoundError(AppException):
    status_code = 404
    detail = 'User not found'


class UserAlreadyExistError(AppException):
    status_code = 400
    detail = 'User already exists'


class InvalidPasswordError(AppException):
    status_code = 400
    detail = 'Invalid password'

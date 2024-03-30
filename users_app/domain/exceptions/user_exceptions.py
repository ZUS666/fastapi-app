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


class UserAlreadyActivatedError(AppException):
    status_code = 400
    detail = 'User already activated'


class InvalidActivationCodeError(AppException):
    status_code = 400
    detail = 'Invalid activation code'


class UserNotActivatedError(AppException):
    status_code = 400
    detail = 'User not activated'

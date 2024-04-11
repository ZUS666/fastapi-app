import enum


class EmailSubject(enum.StrEnum):
    ACTIVATION = 'Activation code'
    RESET_PASSWORD = 'Reset password'

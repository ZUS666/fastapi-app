import enum


class EmailSubject(enum.StrEnum):
    activation_code = "Activation code"
    reset_password = "Reset password"

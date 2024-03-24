import enum


class EmailSubject(enum.StrEnum):
    activation_code = "Activation code"
    reset_password = "Reset password"


class DefaultName(enum.StrEnum):
    first_name = "Your first name could be here, but You didn't tell us it"
    last_name = "Your last name could be here, but You didn't tell us it"


TEMPLATE_MAPPING = {
    EmailSubject.activation_code: 'activation.html',
    EmailSubject.reset_password: 'reset_password.html',
}

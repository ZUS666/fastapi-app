import pytest

from users.services import HashService


@pytest.mark.parametrize(
    'string_password, result', [('password', True), ('password1', True)]
)
def test_hash_service(string_password: str, result: bool) -> None:
    hashed_password = HashService.hash_password(string_password)
    assert HashService.verify_password(string_password, hashed_password) == result

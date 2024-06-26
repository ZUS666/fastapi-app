import re

import pytest


def get_code_capsys(capsys: pytest.CaptureFixture) -> str:
    """Get activation code from stdout."""
    captured = capsys.readouterr().out
    pattern = r"'code': '([^']+)'"
    code = re.search(pattern, captured).group(1)
    return code

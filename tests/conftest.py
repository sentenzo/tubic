import tempfile

import pytest


@pytest.fixture()
def temp_dir() -> str:
    with tempfile.TemporaryDirectory() as temp_dir_path_str:
        yield temp_dir_path_str

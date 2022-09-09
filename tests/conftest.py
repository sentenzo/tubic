import os
import tempfile

import pytest


@pytest.fixture
def temp_dir() -> str:
    with tempfile.TemporaryDirectory() as temp_dir_path_str:
        yield temp_dir_path_str


@pytest.fixture
def change_test_working_dir(temp_dir: str):
    cur_dir = os.getcwd()
    os.chdir(temp_dir)
    yield
    os.chdir(cur_dir)

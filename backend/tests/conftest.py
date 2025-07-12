import os
import pytest

@pytest.fixture(scope='session', autouse=True)
def cleanup_test_db():
    db_path = './test.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    yield
    if os.path.exists(db_path):
        os.remove(db_path) 
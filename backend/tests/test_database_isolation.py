import os


def test_tests_use_a_dedicated_database():
    database_url = os.environ["DATABASE_URL"]

    assert database_url.endswith("/magnify_test")